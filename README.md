# Segmentation of Roads from Satellite Images

Semantic segmentation is the process of classifying each pixel belonging to a particular label. Specifically, in this project, we will identify which region of the satellite image belongs to the road using Deep Learning. 

This project is originally based on the original idea of the following system. A drone will record real-time aerial videos of an unknown area. This video will be sent to a car which will automatically find the best way to go to a specific location of that area. However, we have not had enough knowledge yet to achieve that idea, so we broke it up into a smaller version which is this project. 

Our model is trained based on DeepLab V3+ model and its pre-trained model on Cityscapes Semantic Segmentation Dataset. The training dataset is 8579 satellite images of New York City. Minimal adjustment was done on the initial architecture. The resulted model achieves a satisfying mIoU accuracy of 0.905 (background), 0.768 (road), and 0.836 (overall).
The model is then deployed on a simple website hosted on Google Cloud Platform. The frontend and backend of this website is kept minimal because our main focus in this project is the Deep Learning model itself.

Here is some result images of our deployed model on out-of-dataset input images:
![Image 1](https://raw.githubusercontent.com/dominhnhut01/autodrive_code/master/result1.JPG)
![Image 2](https://raw.githubusercontent.com/dominhnhut01/autodrive_code/master/result2.JPG)
![Image 3](https://raw.githubusercontent.com/dominhnhut01/autodrive_code/master/result3.JPG)

## Content:
1. Collecting and processing the dataset
2. Training the model using DeepLab V3+
3. Deploying the model on a very basic website using simple Flask, HTML, and Javascript.
4. Containerizing the web application and deploy it to Google Cloud Platform
## Collecting and processing the dataset

For this project, we used the satellite images of New York City we crawled on the Internet. I have summed up all the high-quality satellite image in this link. Download and unzip it. All the file format JP2, GEOTIF, and Shapefile contains the coordinate data so it's very convenient for future processing.

### The satellite images
Most of them comes with the format JP2, GEOTIF and their sizes are too large for training. So we need to process the data by cropping them into smaller image and converting them to PNG. First, we need to convert all the JP2 images to GEOTIF by running the Python code at `dataset_collecting\data_convert\jp2_to_tif.py`. 
Then, we need to cutting the large GEOTIF into smaller images without losing any coordinate data (we need this data later to synchronize the image with the road map to create the label). We use the Python code at `dataset_collecting\data_convert\main_export_tif.py`. Finally, we run `dataset_collecting\data_convert\tif_to_jpg.py` and `dataset_collecting\data_convert\2D_to_3D.py` respectively (remember to keep the GEOTIF files for future processing). This code will produce images with different shape in order to prevent the overfitting of the resulted model.

### The label
We will create the label based on the road map data that New York City published on the Internet. It is also included on the above zip file. However, the available data is only the street line and the street center line, but not the mask for the road. Therefore, we will create the mask by ourselves.

First, we need to cut the large map into smaller ones, which must have the synchronous coordinate with the small satellite images that we created earlier. We use the `dataset_collecting\data_convert\shp_to_tif.py` to cut the shapefile with the reference of the previous small GEOTIF satellite images. The result of this code is the tif files, which need to be converted to numpy files with `dataset_collecting\data_convert\tif_to_np.py`. for the next step. 

Next, our idea is separating the numpy file into regions by using the street lines. Then, street center lines will be used to identify which region is and is not the road. We wrote the Python code at `dataset_collecting\annotation\road_annotation.py`. This code will return a folder containing numpy files of road mask. However, some numpy files are broken because of the inconsistency of the data, we need to run `dataset_collecting\annotation\elimination.py` to clean up a bit. This code deletes all the numpy file only containing road or non-road (very irrational, right?)

Unfortunately, the mask label data is not 100% clean up to this point. We still need to manually filter the broken files. So we have to visualize the numpy by converting them to PNG with `dataset_collecting\data_convert\npy_to_png.py` (remember to type "No" for the color-index image option) and manually delete the error images. It's quite laborious but worths it!

Finally, we will use the code `dataset_collecting\data_convert\delete_unfit_files.py` to delete all the satellite images that don't have the mask (I have attached unique ID for each pair image-label so it is uncomplicated). Moreover, we need to turn the previous numpy mask file into color-index PNG with the . Now we have the complete dataset.

### Combine the image and the label into TFRecord
To be used for DeepLab V3+, we must convert the data we created into TFRecord. There are so many tutorial on how to do this so I will leave a link [here](https://medium.com/free-code-camp/how-to-use-deeplab-in-tensorflow-for-object-segmentation-using-deep-learning-a5777290ab6b). I will illustrate this step quickly. 

First, we move the satellite images to `road_segmentation_model\models\research\deeplab\datasets\PQR\dataset\JPEGImages` and color-index PNG mask to `road_segmentation_model\models\research\deeplab\datasets\PQR\dataset\SegmentationClass`. Then, we run the code `road_segmentation_model\models\research\deeplab\datasets\PQR\split_data.py` `road_segmentation_model\models\research\deeplab\datasets\convert_pqr.bat` to split and build the TFRecord data.

## Training the model using DeepLab V3+:

Fortunately, the data scientists from Tensorflow developed an easy-to-use model so it's very easy to train. We only need to run the code `road_segmentation_model\models\research\train.bat` we wrote to train. These batch files only work for Window so you need to write other similar Shell files if you are using Ubuntu. And feel free to modified it to fit your need. To understand more about the training problem, please read this Github repository from @heaversm [link](https://github.com/heaversm/deeplab-training). His instruction is very straight-forward even to beginners.

After completing your training, the resulted model should achieve the approximate mIoU accuracy of 0.905 (background), 0.768 (road), and 0.836 (overall).
Run `road_segmentation_model\models\research\export_model.bat` to export the model to .pb file. This single file will be much more lightweight than the previous trained checkpoint. Then copy it to `deployment\trained_model`, compress it twice until it has a format of `.tar.gz`.

That's done of training! Now we will deploy it on a simple web application.

## Deploying the model on a very basic website using simple Flask, HTML, and Javascript.

We wrote a simple website to deploy this model inside the directory `deployment`. Run the file `main.py` to run it locally. Here is the video demo [link](https://drive.google.com/file/d/168F6VHdxVVyTpg2KmvsgBwGGv4GqYCk1/view).

## Containerizing the web application and deploy it to Google Cloud Platform:

We use Docker to containerize our program. Finally, we upload it to Google Container Registry and host it by Google Kubernetes Engine on Google Cloud Platform. Here is the link of the website: [Road Segmentation model link](http://34.101.141.154:5000/)

#### Created by: 

- Nhut Minh Do (@dominhnhut01)
First year student - Robotics Engineering - Miami University at Ohio '24
- Phu Nhat Tsoi (@PnTsoi)
First year student - Physics - University of California at San Diego '24

#### Reference:
@inproceedings{deeplabv3plus2018,
title={Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation},
author={Liang-Chieh Chen and Yukun Zhu and George Papandreou and Florian Schroff and Hartwig Adam},
booktitle={ECCV},
year={2018}
}
Jerin Paul, Skeyenet - Read Our Planet Like a Book, (2020), GitHub repository,
https://github.com/Paulymorphous/skeyenet



