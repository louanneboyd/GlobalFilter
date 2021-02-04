import cv2
import numpy as np
from filters.helpers.attributes import *

class FadeToColor:

    name = "Fade To Color"

    def __init__(self):

        self.attributes = {
            'Color' :  RGBColorPickerAttribute(),
        }

    def run(self, image, heatmap):
        image = image.astype("float32")
        r,g,b = self.attributes['Color'].value
        color = [b,g,r] # ensure that color is in BGR order (not RGB order)
        image = image * heatmap[:,:,None] + (color * (1 - heatmap[:,:,None])) # lerp between `color` on `image`, using heatmap as the interpolation factor
        return image.astype("uint8")
