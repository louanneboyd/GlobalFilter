import cv2
import math
import numpy as np
from filters.helpers.attributes import *

class ClassicBlur:

    attributes = {
        'kernel size' : Attribute (
            name = 'Blur Amount / Gaussian Kernel Width (pixels)',
            default_value = 81,
            display = ColorPickerDisplay()
        )
    }

    def run(self, image, heatmap):
        blur = lambda kernel_size, sd: cv2.GaussianBlur(image, (kernel_size, kernel_size), sd)
        max_sd_size = 40

        output = np.copy(image)
        heatmap = 1 - heatmap

        for i in range(1, 255):
            sd = max_sd_size * (i/19.)
            # ks = 1 + 2 * math.ceil(sd)
            blurred = blur(81, sd)
            output[:,:,0:2] = 0
            # lerped = image * blurred[:,:,None] + (color * (1 - heatmap[:,:,None])) # lerp
            output[:,:,2] = np.where(heatmap < i/19., output[:,:,2], blurred[:,:,2])

        # cv2.imshow("out", output)



        return output

# def convolve(image, heatmap, x):
