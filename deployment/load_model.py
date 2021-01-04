import os
from io import BytesIO
import tempfile
import tarfile
from six.moves import urllib

#from matplotlib import gridspec
#from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

import tensorflow as tf
from data_handle import CV2_IMAGE, reverse_to_init

class DeepLabModel(object):
	"""Class to load deeplab model and run inference."""

	INPUT_TENSOR_NAME = 'ImageTensor:0'
	OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
	FROZEN_GRAPH_NAME = 'frozen_inference_graph'

	def __init__(self, tarball_path):
		"""Creates and loads pretrained deeplab model."""
		print('Loading model...')
		self.graph = tf.Graph()

		graph_def = None
		# Extract frozen graph from tar archive.
		tar_file = tarfile.open(tarball_path)
		for tar_info in tar_file.getmembers():
			if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
				file_handle = tar_file.extractfile(tar_info)
				graph_def = tf.GraphDef.FromString(file_handle.read())
				break

		tar_file.close()

		if graph_def is None:
			raise RuntimeError('Cannot find inference graph in tar archive.')

		with self.graph.as_default():
			tf.import_graph_def(graph_def, name='')

		self.sess = tf.Session(graph=self.graph)
		print('Model loading complete!')

	def run(self, image):
		"""Runs inference on a single image.

		Args:
			image: A PIL.Image object, raw input image.

		Returns:
			resized_image: RGB image resized from original input image.
			seg_map: Segmentation map of `resized_image`.
		"""
		#Convert 2D image to 3D image
		stacked_img = np.stack((image,)*3, axis=-1)

		batch_seg_map = self.sess.run(
				self.OUTPUT_TENSOR_NAME,
				feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(stacked_img)]})
		seg_map = batch_seg_map[0]
		return stacked_img, seg_map

def create_pascal_label_colormap():
	"""Creates a label colormap used in PASCAL VOC segmentation benchmark.

	Returns:
		A Colormap for visualizing segmentation results.
	"""
	colormap = np.zeros((256, 3), dtype=int)
	ind = np.arange(256, dtype=int)

	for shift in reversed(range(8)):
		for channel in range(3):
			colormap[:, channel] |= ((ind >> channel) & 1) << shift
		ind >>= 3

	return colormap


def label_to_color_image(label):
	"""Adds color defined by the dataset colormap to the label.

	Args:
		label: A 2D array with integer type, storing the segmentation label.

	Returns:
		result: A 2D array with floating type. The element of the array
			is the color indexed by the corresponding element in the input label
			to the PASCAL color map.

	Raises:
		ValueError: If label is not of rank 2 or its value is larger than color
			map maximum entry.
	"""
	if label.ndim != 2:
		raise ValueError('Expect 2-D input label')

	colormap = create_pascal_label_colormap()

	if np.max(label) >= len(colormap):
		raise ValueError('label value too large.')

	return colormap[label]


def vis_segmentation(image, seg_map, LABEL_NAMES, FULL_COLOR_MAP):
	"""Visualizes input image, segmentation map and overlay view."""

	plt.figure(figsize=(15, 5))
	grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

	plt.subplot(grid_spec[0])
	plt.imshow(image)
	plt.axis('off')
	plt.title('input image')

	plt.subplot(grid_spec[1])
	seg_image = label_to_color_image(seg_map).astype(np.uint8)
	plt.imshow(seg_image)
	plt.axis('off')
	plt.title('Prediction segmentation map')

	plt.subplot(grid_spec[2])
	plt.imshow(image)
	plt.imshow(seg_image, alpha=0.7)
	plt.axis('off')
	plt.title('Prediction segmentation overlay')


	unique_labels = np.unique(seg_map)
	ax = plt.subplot(grid_spec[3])
	plt.imshow(
			FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
	ax.yaxis.tick_right()
	plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
	plt.xticks([], [])
	ax.tick_params(width=0.0)
	plt.grid('off')
	plt.show()

def main(MODEL,img_path, unique_key):
	"""
	Predict the segmentation mask of the image

	Parameters:
	- MODEL: The DeepLab object initialized by the class DeepLabModel
	- img_path: string object containing the path to the image
	- unique_key: unique key identifying the request

	Return:
	- Saving the numpy array of the segmentation mask at "templates/temp_img/seg_map_npy_{}.npy".format(unique_key)
	- Saving the JPG image of the segmentation mask at "templates/temp_img/seg_map_{}.jpg".format(unique_key)
	"""

	LABEL_NAMES = np.asarray([
			'background', 'road'
	])
	FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
	FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)

	#Open the image path as a OpenCV object
	img=CV2_IMAGE(img_path)
	
	#Get the initial size of the image
	#Bacause the height, width of CV2 object is in reverse with numpy object
	init_height = img.init_width
	init_width = img.init_height
	print(init_height,init_width)

	#Resize the input image to the input tensor size of the model and turn it into grayscale
	img=img.run()

	#Predict the segmentation map of the image
	image, seg_map=MODEL.run(img)

	#Return to initial size of the input image
	image = reverse_to_init(image,init_height,init_width,'grayscale')
	seg_map = reverse_to_init(seg_map,init_height,init_width,'binary')

	#Save the result
	np.save('templates/temp_img/seg_map_npy_{}.npy'.format(unique_key),seg_map)
	
	PIL_seg_map = Image.fromarray(np.where(seg_map==1,255,seg_map))
	PIL_seg_map = PIL_seg_map.convert('L')
	PIL_seg_map.save('templates/temp_img/seg_map_{}.jpg'.format(unique_key))

	

	#vis_segmentation(image,seg_map,LABEL_NAMES,FULL_COLOR_MAP)
	
	#skeleton, shorest_path=dijksar_algorithm.dijksar(seg_map)
	#dijksar_algorithm.visualization(image,seg_map,skeleton,shorest_path)

if __name__=='__main__':
	main()