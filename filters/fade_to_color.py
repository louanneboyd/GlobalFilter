import cv2
import numpy as np

def run(image, heatmap):
    color = [127, 0, 255]
    image = image.astype("float32")
    image = image * heatmap[:,:,None] + (color * (1 - heatmap[:,:,None])) # lerp between `color` on `image`, using heatmap as the interpolation factor
    return image.astype("uint8")
