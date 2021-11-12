import cv2
import numpy as np
from filters.helpers.attributes import *
import concurrent.futures


class Luminance:

    name = "Luminance"

    def __init__(self):
        self.attributes = {
            'Gray': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True)
        }

    def floor_ceil(self,image):
        image[image > 255] = 255
        image[image < 0] = 0
        return image

    def run(self, image, heatmap):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32") # convert image to HSV colorspace. use float32 for more precision
        heatmap = heatmap.astype("float32")

        h_channel, s_channel, v_channel = cv2.split(hsv)
        v_channel -= (heatmap.max() - heatmap)*255*self.attributes['Gray'].value/10
        v_channel = self.floor_ceil(v_channel)

        hsv_n = cv2.merge((h_channel, s_channel, v_channel))

        image = cv2.cvtColor(hsv_n.astype("uint8"), cv2.COLOR_HSV2BGR) # convert back to uint8 type and BGR colorspace
        return image
