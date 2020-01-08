# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:39:33 2020

@author: Brandon Makin
"""

import numpy as np
from PIL import Image
import os

class Filterizer:
    def __init__(self, photos_directory, heatmaps_directory, output_directory):
        self.__photos_directory = photos_directory
        self.__heatmaps_directory = heatmaps_directory
        self.__output_directory = output_directory
    
    def get_heatmap(self):
        return self.__heatmap_array
    
    def get_photo(self):
        assert self.__color_mode != None, "There's a problem with your filter: \nPlease call set_color_mode(mode) before calling get_photo(). \nPossible color modes include 'RGB' and 'HSV'"
        data = np.array(self.__photo_image.convert(self.__color_mode)) # set image to currect color mode (ex. RGB, HSV) and convert to numpy array
        data = data.astype(np.float32) # convert photo data from ubyte to float32, so we can do float division
        return data
    
    def set_color_mode(self, color_mode = 'rgb'):
        self.__color_mode = color_mode
    
    def run_filter(self, filter):
        print(f'Running the filter "{filter.__name__}" and saving the new photos to "{self.__output_directory}"\n...')
        self.__color_mode = None
        for i, photo_file in enumerate(os.listdir(self.__photos_directory)):
            heatmap_filepath = self.__heatmaps_directory + os.listdir(self.__heatmaps_directory)[i]
            photo_filepath = self.__photos_directory + photo_file
            # load current photo and heatmap
            with Image.open(photo_filepath) as image, Image.open(heatmap_filepath) as heatmap_image:
                self.__photo_image = image
                self.__heatmap_array = self.__get_heatmap_array_from_image(heatmap_image)
                data = filter(self)
                assert (data is not None), "There's a problem with your filter: \nA filter must always return the modified photo data (as a numpy array). \nMake sure your function ends with something that looks like: \n>>  return photo"
                data = data.astype(np.ubyte)
                # convert back to image and display
                if (self.__color_mode == None):
                    self.__color_mode = 'RGB'
                new_photo = Image.fromarray(data, mode=self.__color_mode)
                new_photo.save(self.__output_directory + photo_file) # save in the output directory, using the image file's original name
        print("Done")
    
    def __get_heatmap_array_from_image(self, heatmap_image):
        heatmap = np.array(heatmap_image) # convert image to numpy array
        if (len(np.shape(heatmap)) == 3): # check if heatmap is 3-dimensional, i.e. if (in addition to x and y dimensions) this image has rgb(a)
            # if this heatmap matrix does have more than one color channel, remove all but one.
            # we only need to use one channel of the heatmap all 3 channels are equal
            heatmap = heatmap[:,:,0]
        heatmap = heatmap.astype(np.float32) # convert hsv data from ubyte to float32, so we can do float division
        heatmap /= 255.0 # heatmap was in the range of 0-255. now it's in the range of 0.0 - 1.0
        return heatmap