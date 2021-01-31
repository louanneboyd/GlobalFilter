import cv2
import math
import numpy as np
from filters.helpers.attributes import *

class AccurateBlur:

    name = "Blur (Accurate)"

    attributes = {
        'kernel size' : Attribute (
            name = 'Blur Amount / Gaussian Kernel Width (pixels)',
            default_value = 81,
            display = ColorPickerDisplay()
        )
    }

    def run(self, image, heatmap):

        image = image.astype("float32")

        # largest standard deviation for max blur
        max_sd = 8
        kernel_radius = math.ceil(max_sd) * 2

        padded = np.pad(image, pad_width=kernel_radius, mode='edge') # pad image for correct blurring at edges

        v_convolve = np.vectorize(convolve, excluded=[0])
        # get coords for each point
        y_coords, x_coords = np.indices(np.shape(image[:,:,0]))
        # cv2.imshow("y", y_coords/600)
        # cv2.imshow("x", x_coords/800)
        heatmap = 1-heatmap
        image[:,:,0] = v_convolve(padded[:,:,0], x_coords + kernel_radius, y_coords + kernel_radius, heatmap, max_sd)
        image[:,:,1] = v_convolve(padded[:,:,1], x_coords + kernel_radius, y_coords + kernel_radius, heatmap, max_sd)
        image[:,:,2] = v_convolve(padded[:,:,2], x_coords + kernel_radius, y_coords + kernel_radius, heatmap, max_sd)



        # for color_channel in range(len(cv2.split(image))):
        #     for x in range(len(image)): # height
        #         for y in range(len(image[0])): # width
        #             px = convolve(padded[:,:,color_channel], x, y, heatmap[x,y], max_sd)
        #             image[x,y, color_channel] = px
        #             # print(color_channel)
        #             # image[x,y,color_channel] = heatmap[x,y] * 255
        #

        # image[:,:,0] = heatmap * 255
        # image[:,:,1] = heatmap
        # image[:,:,2] = heatmap
        # image = heatmap
        return image.astype("uint8")

def convolve(image_matrix, y, x, heatmap_pixel, max_sd):

    # standard deviation
    sd = heatmap_pixel * max_sd

    # kernel radius should always be at least 2*sd
    kernel_radius = math.ceil(sd) * 2 # todo: possible performance increase by shrinking kernel_radius to match sd instead of max_sd
    kernel_size = kernel_radius * 2 + 1

    # section of the image matrix that we convolve for the current pixel
    subarray = image_matrix[x-kernel_radius : x+kernel_radius+1, y-kernel_radius : y+kernel_radius+1]

    # todo: generate Gaussian kernel.
    # todo: replace box blur with Gaussian blur
    # result = np.average(subarray)
    result = np.average(subarray, weights=getGaussianKernel2D(kernel_size, sd))

    return result


def getGaussianKernel2D(ksize, sigma):
    k_1d = cv2.getGaussianKernel(ksize, sigma)
    return np.dot(k_1d, k_1d.T)
