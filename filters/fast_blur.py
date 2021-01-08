import cv2
import numpy as np

def run(image, heatmap):
    gaussian_kernel_size = 101 # must be an odd number. controls the maximum amount of blur
    blurred_image = cv2.GaussianBlur(image, (gaussian_kernel_size, gaussian_kernel_size), 0)
    final = image * heatmap[:,:,None] + (blurred_image * (1 - heatmap[:,:,None])) # lerp between `blurred_image` on `image`, using heatmap as the interpolation factor

    return final.astype("uint8")
