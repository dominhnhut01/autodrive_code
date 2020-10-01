import numpy as np
import tensorflow as tf
import os
import IPython.display as display
import PIL

in_direc = "/home/tsoi/Yours/Projects/SDC/data/main_dataset/tfrecords/data.tfrecords"

def read_record(directory):
    raw_data = tf.data.TFRecordDataset(directory)
    feature_description = {
        'height': tf.io.FixedLenFeature([1],tf.int64),
        'width': tf.io.FixedLenFeature([1],tf.int64),
        'depth': tf.io.FixedLenFeature([1],tf.int64),
        'label': tf.io.FixedLenFeature([1],tf.int64),
        'image': tf.io.FixedLenFeature((),tf.string),
        'numpy': tf.io.FixedLenFeature([873,441],tf.int64)
    }
    def _parse_image_function(example_proto):
        # Parse the input `tf.train.Example` proto using the dictionary above.
        return tf.io.parse_single_example(example_proto, feature_description)
    parsed_image_dataset = raw_data.map(_parse_image_function)
    #print(parsed_image_dataset)
    for image_features in parsed_image_dataset:
        image_raw = image_features['image'].numpy()
        display.display(display.Image(data=image_raw))
        #print(image_raw)
'''
for image_features in parsed_image_dataset:
    image_raw = image_features['image_raw'].numpy()
    display.display(display.Image(data=image_raw))
'''

read_record(in_direc)
