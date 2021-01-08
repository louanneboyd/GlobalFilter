import cv2
import numpy as np
from filters.helpers.attributes import *

class FadeToColor:

    attributes = {
        'color' : Attribute (
            name = 'Color',
            default_value = [0, 0, 0],
            display = ColorPickerDisplay()
        )
    }

    def run(self, image, heatmap):
        image = image.astype("float32")
        color = self.attributes['color'].value
        image = image * heatmap[:,:,None] + (color * (1 - heatmap[:,:,None])) # lerp between `color` on `image`, using heatmap as the interpolation factor
        return image.astype("uint8")
