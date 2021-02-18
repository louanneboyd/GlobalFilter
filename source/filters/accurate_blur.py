import cv2
import math
import numpy as np
from filters.helpers.attributes import *
import concurrent.futures

class AccurateBlur:

    name = "Blur (Accurate)"

    def __init__(self):
        self.attributes = {
            'Blur Amount / Standard Deviation': SliderAttribute(default = 8, min = 0, max = 10, step = 1, clampInput = True),
        }

    def run(self, image, heatmap):

        image = image.astype("float32")

        max_sd = self.attributes['Blur Amount / Standard Deviation'].value # largest standard deviation for max blur
        if max_sd > 0:

            # largest standard deviation for max blur
            max_kernel_radius = math.ceil(max_sd) * 2

            padded = np.pad(image, pad_width=max_kernel_radius, mode='edge') # pad image for correct blurring at edges

            v_convolve = np.vectorize(convolve, excluded=[0])
            # get coords for each point
            y_coords, x_coords = np.indices(np.shape(image[:,:,0]))
            # cv2.imshow("y", y_coords/600)
            # cv2.imshow("x", x_coords/800)
            heatmap = 1-heatmap
            b,g,r = cv2.split(image)
            b_padded = np.pad(b, pad_width=max_kernel_radius, mode='edge') # pad image for correct blurring at edges
            g_padded = np.pad(g, pad_width=max_kernel_radius, mode='edge') # pad image for correct blurring at edges
            r_padded = np.pad(r, pad_width=max_kernel_radius, mode='edge') # pad image for correct blurring at edges

            lam_b = lambda: v_convolve(b_padded, x_coords + max_kernel_radius, y_coords + max_kernel_radius, heatmap, max_sd)
            lam_g = lambda: v_convolve(g_padded, x_coords + max_kernel_radius, y_coords + max_kernel_radius, heatmap, max_sd)
            lam_r = lambda: v_convolve(r_padded, x_coords + max_kernel_radius, y_coords + max_kernel_radius, heatmap, max_sd)
            # lam_b = lambda: b
            # lam_g = lambda: g
            # lam_r = lambda: r

            # filter each channel on a separate thread to speed up this slow filter.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                t1 = executor.submit(lam_b)
                t2 = executor.submit(lam_g)
                t3 = executor.submit(lam_r)

                b = t1.result()
                g = t2.result()
                r = t3.result()

                image = cv2.merge((b,g,r))
                # print(b.shape)
                # print(g.shape)
                # image = b
        return image.astype("uint8")

def convolve(image_matrix, y, x, heatmap_pixel, max_sd):

    # standard deviation
    sd = heatmap_pixel * max_sd

    # kernel radius should always be at least 2*sd
    kernel_radius = math.ceil(sd) * 2
    kernel_size = kernel_radius * 2 + 1

    # section of the image matrix that we convolve for the current pixel
    subarray = image_matrix[x-kernel_radius : x+kernel_radius+1, y-kernel_radius : y+kernel_radius+1]

    result = np.average(subarray, weights=getGaussianKernel2D(kernel_size, sd))

    return result


def getGaussianKernel2D(ksize, sigma):
    k_1d = cv2.getGaussianKernel(ksize, sigma)
    return np.dot(k_1d, k_1d.T)
