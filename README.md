# Segmentation of Roads from Satellite images

Semantic segmentation is the process of classifying each pixel belonging to a particular label. Specifically, in this project, we will identify which region of the satellite image belongs to the road using Deep Learning. Our model is trained based on DeepLab V3+ model and its pre-trained model on Cityscapes Semantic Segmentation Dataset. Minimal adjustment was done on the initial architecture. The resulted model achieves a satisfying mIoU accuracy of 0.905 (background), 0.768 (road), and 0.836 (overall).
The model is then deployed on a simple website hosted on Google Cloud Platform. The frontend and backend of this website is kept minimal because our main focus in this project is the Deep Learning model itself.

## Content:
1. Collecting and processing the dataset
2. Training the model using DeepLab V3+
3. Deploying the model on a very basic website using simple Flask, HTML, and Javascript.

## Collecting and processing the dataset

For this project, I used the satellite images of New York City I found on the Internet. I have sum up all the high-quality satellite image in this link. Download and unzip it. All the file format JP2, GEOTIF, and Shapefile contains the coordinate data so it's very convenient for future processing

### The satellite images
Most of them comes with the format JP2, GEOTIF and their sizes are too large for training. So we need to process the data by cropping them into smaller image and converting them to PNG. First, we need to convert all the JP2 images to GEOTIF by running the Python code at `dataset_collecting\data_convert\jp2_to_tif.py`. 
Then, we need to cutting the large GEOTIF into smaller images without losing any coordinate data (we need this data later to synchronize the image with the road map to create the label). We use the Python code at `dataset_collecting\data_convert\main_export_tif.py`. Finally, we run `dataset_collecting\data_convert\tif_to_jpg.py` and `dataset_collecting\data_convert\2D_to_3D.py` respectively (remember to keep the GEOTIF files for future processing).

### The label
We will create the label based on the road map data that New York City published on the Internet. It is also included on the above zip file. However, the available data is only the street line and the street center line, but not the mask for the road. Therefore, we will create the mask by ourselves.
First, we need to cut the large map into smaller ones, which must have the synchronous coordinate with the small satellite images that we created earlier. We use the `dataset_collecting\data_convert\shp_to_tif.py` to cut the shapefile with the reference of the previous small GEOTIF satellite images. The result of this code is the tif files, which need to be converted to numpy files with `dataset_collecting\data_convert\tif_to_np.py`. for the next step. 
Next, our idea is separating the numpy file into regions by using the street lines. Then, street center lines will be used to identify which region is and is not the road. We wrote the Python code at `dataset_collecting\annotation\road_annotation.py`. This code will return a folder containing numpy files of road mask. However, some numpy files are broken because of the inconsistency of the data, we need to run `dataset_collecting\annotation\elimination.py` to clean up a bit. This code deletes all the numpy file only containing road or non-road (very irrational, right?)
Unfortunately, the mask label data is not 100% clean up to this point. We still need to manually filter the broken files. So we have to visualize the numpy by converting them to PNG with `dataset_collecting\data_convert\npy_to_png.py` (remember to type "No" for the color-index image option) and manually delete the error images. It's quite laborious but worths it!
Finally, we will use the code `dataset_collecting\data_convert\delete_unfit_files.py` to delete all the satellite images that don't have the mask (I have attached unique ID for each pair image-label so it is uncomplicated). Moreover, we need to turn the previous numpy mask file into color-index PNG with the . Now we have the complete dataset.

### Combine the image and the label into TFRecord
To be used for DeepLab V3+, we must convert the data we created into TFRecord. There are so many tutorial on how to do this so I will leave a link [here](https://medium.com/free-code-camp/how-to-use-deeplab-in-tensorflow-for-object-segmentation-using-deep-learning-a5777290ab6b). I will illustrate this step quickly. 
First, we 

