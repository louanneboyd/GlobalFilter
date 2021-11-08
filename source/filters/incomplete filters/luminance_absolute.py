import cv2
import numpy as np
from filters.helpers.attributes import *
import concurrent.futures


class Luminance:

    name = "Luminance"

    def __init__(self):
        self.attributes = {
            'Gray': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True),
            'Thresh': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True),
            'Alpha': SliderAttribute(default = 2, min = -10, max = 10, step = 1, clampInput = True),
            'Weight': SliderAttribute(default = 5, min = 0, max = 10, step = 1, clampInput = True)

        }
    def floor_ceil(self,image):
        image[image > 255] = 255
        image[image < 0] = 0
        return image

    def run(self, image, heatmap):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32") # convert image to HSV colorspace. use float32 for more precision
        #hsv[:,:,2] *= heatmap*self.attributes['Luminance'].value # multiply saturation by heatmap
        #print(heatmap.shape)
        #create heatmap with alpha
        #hsv_hm = cv2.cvtColor(heatmap, cv2.COLOR_BGR2HSV).astype("float32")
        #return (hsv * (heatmap[:,:,None]*10)).astype("uint8")
        #print(hsv_hm.shape)

        h_channel, s_channel, v_channel = cv2.split(hsv)
        print(h_channel.max())
        heatmap = heatmap.astype("float32")
        print(heatmap.max())
        v_channel -= (heatmap.max() - heatmap)*255*self.attributes['Gray'].value/10
        v_channel = self.floor_ceil(v_channel)


        #a_channel = np.ones(h_channel.shape, dtype=h_channel.dtype)
        hsv_n = cv2.merge((h_channel, s_channel, v_channel))

        image = cv2.cvtColor(hsv_n.astype("uint8"), cv2.COLOR_HSV2BGR) # convert back to uint8 type and BGR colorspace
        return image
        print(type(heatmap))
        print(type(image))

        mask = np.zeros(heatmap.shape, dtype="uint8")
        mask[heatmap.astype("float32") > self.attributes['Thresh'].value/10] = 255

        gray = np.ones(heatmap.shape, dtype="float32")*self.attributes['Gray'].value*10


        print(mask)

        return mask

        '''

        h_channel = np.zeros(heatmap.shape, dtype=heatmap.dtype)
        s_channel = np.zeros(heatmap.shape, dtype=heatmap.dtype)
        a_channel = heatmap.astype("float32") * 255 * self.attributes['Alpha'].value
        #print(v_channel)
        v_channel = np.zeros(heatmap.shape, dtype=heatmap.dtype)
        hsva_hm = cv2.merge(( h_channel, s_channel, v_channel, a_channel ))

        #add alpha to hsv
        h_channel, s_channel, v_channel = cv2.split(hsv)
        a_channel = np.ones(h_channel.shape, dtype=h_channel.dtype)
        hsva = cv2.merge((h_channel, s_channel, v_channel, a_channel))

        #hsva = np.concatenate([hsv, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        #hsva_t = hsv.copy()#np.all(hsv == [255, 255, 255], axis=-1)
        #hsva_t[:,:,3] = hsva_t[:,:,2] * self.attributes['Luminance'].value
        weighted = cv2.addWeighted(hsva, self.attributes['Weight'].value/10.0, hsva_hm, (10 - self.attributes['Alpha'].value)/10.0, 0)
        print(weighted.shape)
        h_channel, s_channel, v_channel, a_channel = cv2.split(weighted)
        hsv_n = cv2.merge((h_channel, s_channel, v_channel))
        image = cv2.cvtColor(hsv_n.astype("uint8"), cv2.COLOR_HSV2BGR) # convert back to uint8 type and BGR colorspace
        return image

        '''
