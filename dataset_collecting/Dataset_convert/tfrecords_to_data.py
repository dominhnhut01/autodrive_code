import numpy as np
import tensorflow as tf
import os
import IPython.display as display
import PIL

def read_record(in_dir):
    # Read the TFRecord file
    raw_data = tf.data.TFRecordDataset(in_dir)
    feature_description = {
        'height': tf.io.FixedLenFeature([1],tf.int64),
        'width': tf.io.FixedLenFeature([1],tf.int64),
        'depth': tf.io.FixedLenFeature([1],tf.int64),
        'label': tf.io.FixedLenFeature([1],tf.int64),
        'image': tf.io.FixedLenFeature((),tf.string),
        'numpy': tf.io.FixedLenFeature([873,441],tf.int64)
    }
    def _parse_image_function(example_proto):
        # Parse the input tf.train.Example proto using the dictionary above.
        return tf.io.parse_single_example(example_proto, feature_description)
    parsed_image_dataset = raw_data.map(_parse_image_function)
    #print(parsed_image_dataset)
    for image_features in parsed_image_dataset:
        image_raw = image_features['image'].numpy()
        display.display(display.Image(data=image_raw))
        #print(image_raw)
'''
Test code:
for image_features in parsed_image_dataset:
    image_raw = image_features['image_raw'].numpy()
    display.display(display.Image(data=image_raw))
'''
if _name_ == '_main_':

    #Get the current directory
    os.chdir('../../../dataset/')
    main_dir = os.getcwd()
    in_file = input("Enter input TFRecord file name here: ")

    #Create absolute path:
    in_dir = os.path.join(main_dir,in_file)
    read_record(in_dir)
