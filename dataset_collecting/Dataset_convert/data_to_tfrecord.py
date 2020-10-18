import numpy as np
import tensorflow as tf
import os
import PIL
'''
This code takes in jpg images (since tf can't read tiff) to save it as a feature in TFrecord
so you should run tif_to_jpg.py first.
'''

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

in_direc_jpg = "/home/tsoi/Yours/Projects/SDC/data/main_dataset/satellite_jpg"
in_direc_npy = "/home/tsoi/Yours/Projects/SDC/data/main_dataset/street_annotate_npy"
out_direc = "/home/tsoi/Yours/Projects/SDC/data/main_dataset/tfrecords"

def write_record(label,img_string,npy,out_direc,width,height, tfrecord_name):
    feature = {
        'height': _int64_feature([height]),
        'width': _int64_feature([width]),
        'depth': _int64_feature([1]),
        'label': _int64_feature([int(label)]),
        'image': _bytes_feature(img_string),
        'numpy': _int64_feature(npy)
    }
    tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
    with tf.io.TFRecordWriter(out_direc+"/"+str(tfrecord_name)+'.tfrecords') as writer:
        writer.write(tf_example.SerializeToString())

def serialize_array(array):
  array = tf.io.serialize_tensor(array)
  return array

def tfrecord_write_from_folder(in_direc_jpg,in_direc_npy,out_direc):
    JPGs = os.listdir(in_direc_jpg)
    NPYs = os.listdir(in_direc_npy)
    file_number = 0
    tfrecord_name = 0
    for jpg in JPGs:
        jpg_direc = in_direc_jpg+"/"+jpg
        img_string = open(jpg_direc,'rb').read()
        image = PIL.Image.open(jpg_direc)
        width, height = image.size
        name = jpg[4:-4]
        numpy_data = np.load(in_direc_npy+"/"+"street_data_"+name+".npy")
        numpy_data= numpy_data.reshape((1,width*height))
        npy = numpy_data[0]
        #npy = numpy_data.tolist()
        write_record(name,img_string,npy,out_direc,width,height,name)


if __name__ == "__main__":
    
    #Get the current directory
    os.chdir('../../../dataset/')
    main_dir = os.getcwd()

    #img files are the image file
    #NPY files are the annotation mask
    img_folder = input("Enter img folder name here: ")
    mask_folder = input("Enter npy folder name here: ")
    out_folder = input("Enter output folder + file name here: ")
    '''
    #Create absolute path:
    '''
    img_dir = os.path.join(main_dir,img_folder)
    mask_dir = os.path.join(main_dir,mask_folder)
    out_dir = os.path.join(main_dir,out_folder)
    
    tfrecord_write_from_folder(img_dir,mask_dir,out_dir)
