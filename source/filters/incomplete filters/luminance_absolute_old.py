import cv2
import numpy as np
from filters.helpers.attributes import *
import concurrent.futures


class LuminanceAbsolute:

    name = "Absolute Luminance"

    def __init__(self):
        self.attributes = {
            'Gray': SliderAttribute(default = 4, min = 0, max = 10, step = 1, clampInput = True),
            'Thresh': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True)
        }
    def floor_ceil(self,image):
        image[image > 255] = 255
        image[image < 0] = 0
        return image

    def run(self, image, heatmap):

        mask = np.zeros(heatmap.shape, dtype="float32")
        mask[heatmap.astype("float32") < self.attributes['Thresh'].value/10] = 1

        #hsv_n = cv2.merge((np.zeros(heatmap.shape, dtype="float32"),
        #                   np.zeros(heatmap.shape, dtype="float32"),
        #                   mask))

        #image = cv2.cvtColor(hsv_n.astype("uint8"), cv2.COLOR_HSV2BGR) # convert back to uint8 type and BGR colorspace
        #return image
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32") # convert image to HSV colorspace. use float32 for more precision

        h_channel, s_channel, v_channel = cv2.split(hsv)
        v_channel = mask*255.0*self.attributes['Gray'].value/10
        v_channel = v_channel.clip(0,255)

        '''
        mask_index = mask>=1
        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if mask[i,j]>=1:
                    v_channel[i,j] = 255.0*self.attributes['Gray'].value/10
        '''
        #print(mask_index.shape)
        #print(np.indices(mask_index.shape)[mask_index])
        #v_channel[mask>=1] = mask*255.0*self.attributes['Gray'].value/10
        #v_channel[mask<1] = v_channel[mask<1]
        #hsv[:,:,2] = mask*255.0*self.attributes['Gray'].value/10
        #hsv[:,:,2] = self.floor_ceil(v_channel)

        '''
        print(h_channel.shape)
        print(v_channel.shape)
        print(h_channel.max())
        print(v_channel.max())
        '''
        #print(hsv.shape)

        hsv_n = cv2.merge((h_channel, s_channel, v_channel))

        image = cv2.cvtColor(hsv_n.astype("uint8"), cv2.COLOR_HSV2BGR) # convert back to uint8 type and BGR colorspace
        return image
