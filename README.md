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
Then, we need to cutting the large GEOTIF into smaller images without losing any coordinate data (we need this data later to synchronize the image with the road map to create the label). We use the Python code at `dataset_collecting\data_convert\main_export_tif.py`. 

### The label
We will create the label based on the road map data that New York City published on the Internet. It is also included on the above zip file. However, the available data is only the street line and the street center line, but not the mask for the road. Therefore, we will create the mask by ourselves.
First, we need to cut the large map into smaller ones, which must have the synchronous coordinate with the small satellite images that we created earlier. We use the `dataset_collecting\data_convert\shp_to_tif.py` to cut the shapefile with the reference of the previous small satellite images. The result of this code is the tif files, which need to be converted to numpy files for the next step. 
Next, our idea is separating the numpy file into 
