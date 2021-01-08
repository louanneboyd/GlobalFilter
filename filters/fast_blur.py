import cv2
import numpy as np
from filters.helpers.attributes import *

class FastBlur:

    attributes = {
        'kernel size' : Attribute (
            name = 'Blur Amount / Gaussian Kernel Width (pixels)',
            default_value = 81,
            display = ColorPickerDisplay()
        )
    }

    def run(self, image, heatmap):
        kernel_size = self.attributes['kernel size'].value # must be an odd number. controls the maximum amount of blur
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        final = image * heatmap[:,:,None] + (blurred_image * (1 - heatmap[:,:,None])) # lerp between `blurred_image` on `image`, using heatmap as the interpolation factor

        return final.astype("uint8")
