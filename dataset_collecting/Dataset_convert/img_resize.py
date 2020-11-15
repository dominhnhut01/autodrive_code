from PIL import Image
import os

direc = 'E:/college_projects/autodrive_car/dataset/output_tif/supporting_dataset/test_dataset'
new_direc = 'E:/college_projects/autodrive_car/dataset/output_tif/supporting_dataset/test_dataset'
for file in os.listdir(direc):
	filename = file[:-4]
	n_width = 220
	n_len = 436
	img=Image.open('{}/{}'.format(direc,file))
	img = img.resize((n_len,n_width), Image.ANTIALIAS)
	img.save('{}/{}.png'.format(new_direc,filename))