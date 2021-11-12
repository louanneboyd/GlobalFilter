import cv2
import numpy as np
from filters.helpers.attributes import *
import concurrent.futures


class LuminanceAbsolute:

    name = "Absolute Luminance"

    def __init__(self):
        self.attributes = {
            'Max Brightness': SliderAttribute(default = 4, min = 0, max = 10, step = 1, clampInput = True),
            'Thresh': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True)
        }

    def run(self, image, heatmap):

        mask = np.zeros(heatmap.shape, dtype="float32")
        mask[heatmap.astype("float32") < self.attributes['Thresh'].value/10] = 255

        mask3 = cv2.merge((mask, mask, mask))#np.dstack([mask, mask, mask])
        image = image.astype("float32")
        image_bg_only = image[mask>=1]
        image_bg = cv2.bitwise_and(image, mask3)

        cols, rows = image_bg_only.shape

        brightness = np.sum(image_bg_only) / (255 * cols * rows)
        minimum_brightness = 1.0*self.attributes['Max Brightness'].value/10

        ratio = brightness / minimum_brightness
        adj_image_bg = cv2.convertScaleAbs(image_bg, alpha = 1, beta = 255 * (minimum_brightness - brightness))

        image_new = image.copy()
        image_new[np.where(mask3==(255,255,255))] = adj_image_bg[np.where(mask3==(255,255,255))]

        return image_new.astype("uint8")
        '''
        # devnote: modify this to either darken background or lighten foreground
        if ratio >= 1:
            print("Image already dark enough")
            pass
        else:
            return cv2.convertScaleAbs(img, alpha = 1 / ratio, beta = 0)
        '''
