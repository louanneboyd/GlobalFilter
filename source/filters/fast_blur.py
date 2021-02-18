import cv2
import numpy as np
from filters.helpers.attributes import *

class FastBlur:

    name = "Blur (Fast)"

    def __init__(self):
        self.attributes = {
            'Blur Amount / Kernel Radius': SliderAttribute(default = 40, min = 0, max = 500, step = 1, clampInput = True),
        }

    def run(self, image, heatmap):
        kernel_size = (self.attributes['Blur Amount / Kernel Radius'].value // 1) * 2 + 1 # double the radius. must be an odd number. controls the maximum amount of blur
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        final = image * heatmap[:,:,None] + (blurred_image * (1 - heatmap[:,:,None])) # lerp between `blurred_image` on `image`, using heatmap as the interpolation factor

        return final.astype("uint8")
