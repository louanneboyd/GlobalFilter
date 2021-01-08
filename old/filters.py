# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:54:10 2020

@author: Brandon Makin
"""

import filterizer

photos_directory = "data/first 50 images/input/images/"
heatmaps_directory = "data/first 50 images/input/heatmaps/"
output_directory = "data/output/"

example_image = photos_directory + "01.jpg"
example_heatmap = heatmaps_directory + "n01.jpg"

f = filterizer.Filterizer(photos_directory, heatmaps_directory, output_directory)

def desaturate(filterizer):
    # set color mode to HSV, because we want to be modifying saturation
    filterizer.set_color_mode('HSV')
    
    # get raw data
    photo = filterizer.get_photo()
    heatmap = filterizer.get_heatmap()
    
    # quick references to HSV channels
    hue = photo[:,:,0]
    saturation = photo[:,:,1]
    value = photo[:,:,2]
    
    # modify image
    saturation *= heatmap

    # save modified image
    filterizer.set_photo(photo)

def __lerp(a, b, amount):
    return a * (1 - amount) + b * amount

def blend_to_gray_linear(filterizer):
    # we always have to set the color mode before getting the picture
    filterizer.set_color_mode('RGB')
    
    # get raw data
    photo = filterizer.get_photo()
    heatmap = filterizer.get_heatmap()
    
    # modify image
    gray = 255
    photo[:,:,0] = __lerp(photo[:,:,0], gray, 1 - heatmap)
    photo[:,:,1] = __lerp(photo[:,:,1], gray, 1 - heatmap)
    photo[:,:,2] = __lerp(photo[:,:,2], gray, 1 - heatmap)
    
    filterizer.set_photo(photo)

def blend_to_gray_quadratic(filterizer):
    # we always have to set the color mode before getting the picture
    filterizer.set_color_mode('RGB')
    
    # get raw data
    photo = filterizer.get_photo()
    heatmap = filterizer.get_heatmap()
    
    # modify image
    gray = 255/2
    blend_factor = 1 - (heatmap * heatmap)
    photo[:,:,0] = __lerp(photo[:,:,0], gray, blend_factor)
    photo[:,:,1] = __lerp(photo[:,:,1], gray, blend_factor)
    photo[:,:,2] = __lerp(photo[:,:,2], gray, blend_factor)
    
    filterizer.set_photo(photo)

f.run_filter(blend_to_gray_linear)