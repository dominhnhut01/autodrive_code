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

def write_record(label,img_string,npy,out_dir,width,height):
    feature = {
        'height': _int64_feature([height]),
        'width': _int64_feature([width]),
        'depth': _int64_feature([1]),
        'label': _int64_feature([int(label)]),
        'image': _bytes_feature(img_string),
        'numpy': _int64_feature(npy)
    }
    tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
    with tf.io.TFRecordWriter(out_dir+"/"+'data.tfrecords') as writer:
        writer.write(tf_example.SerializeToString())

def serialize_array(array):
  array = tf.io.serialize_tensor(array)
  return array

def tfrecord_write_from_folder(img_dir,mask_dir,out_dir):
    IMGs = os.listdir(img_dir)
    MASKs = os.listdir(mask_dir)
    for img in IMGs:
        img_new_dir = img_dir+"/"+img
        img_string = open(img_new_dir,'rb').read()
        image = PIL.Image.open(img_new_dir)
        width, height = image.size
        name = img[4:-4]
        mask_data = np.load(mask_dir+"/"+"street_data_"+name+".npy")
        mask_data= mask_data.reshape((1,width*height))
        mask = mask_data[0]
        #mask = mask_data.tolist()
        write_record(name,img_string,mask,out_dir,width,height)

if __name__ == '__main__':
    
    #Get the current directory
    os.chdir('../../../dataset/')
    main_dir = os.getcwd()
    
    #img files are the image file
    #NPY files are the annotation mask
    img_folder = input("Enter img folder name here: ")
    mask_folder = input("Enter npy folder name here: ")
    out_folder = input("Enter output folder + file name here: ")
    
    #Create absolute path:
    img_dir = os.path.join(main_dir,img_folder)
    mask_dir = os.path.join(main_dir,mask_folder)
    out_dir = os.path.join(main_dir,out_folder)

    tfrecord_write_from_folder(img_dir,mask_dir,out_dir)
