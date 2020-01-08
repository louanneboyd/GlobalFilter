# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:39:33 2020

@author: Brandon Makin
"""

import numpy as np
from PIL import Image
import matplotlib.colors as color

directory_input_heatmaps = "data/first 50 images/input/heatmaps/"
directory_input_images = "data/first 50 images/input/images/"
directory_output = "data/output/"

example_image = directory_input_images + "01.jpg"
example_heatmap = directory_input_heatmaps + "n01.jpg"

def get_heatmap_data_from_image(heatmap_image):
    heatmap = np.array(heatmap_image) # convert image to numpy array
    heatmap = heatmap.astype(np.float32) # convert hsv data from ubyte to float32, so we can do float division
    heatmap = heatmap[:,:,0] # we only need to use one channel of the heatmap all 3 channels are equal
    heatmap /= 255.0 # heatmap was in the range of 0-255. now it's in the range of 0.0 - 1.0
    return heatmap

def get_photo_data_from_image(image, color_mode):
    hsv = np.array(image.convert(color_mode)) # set image to HSV mode (instead of RGB) as convert to numpy array
    hsv = hsv.astype(np.float32) # convert hsv data from ubyte to float32, so we can do float division
    return hsv

def apply_filter(photo_filepath, heatmap_filepath, filter_function, photo_color_mode="RGB"):
    with Image.open(photo_filepath) as image, Image.open(heatmap_filepath) as heatmap_image:
        # get data
        photo = get_photo_data_from_image(image, photo_color_mode)
        heatmap = get_heatmap_data_from_image(heatmap_image)
        
        # apply filter (call filter_function)
        filter_function(photo, heatmap)
        
        # convert back to image and display
        photo = photo.astype(np.ubyte)
        new_image = Image.fromarray(photo, mode=photo_color_mode)
        new_image.show()
        #heatmap_image.show()

def desaturate(image_data, heatmap):
    # quick references to hsv channels
    hue = image_data[:,:,0]
    saturation = image_data[:,:,1]
    value = image_data[:,:,2]
    
    #modify image
    saturation *= heatmap
    
apply_filter(example_image, example_heatmap, desaturate, photo_color_mode="HSV")
