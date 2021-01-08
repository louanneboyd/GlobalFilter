import cv2
from tkinter import Tk
from tkinter.filedialog import askdirectory

import model
import filters.desaturate
import filters.fade_to_color
import filters.fast_blur

# Ask the user for the image folder and the heatmap folder
# Tk().withdraw()
# filename = askdirectory(initialdir = ".", title = "Select folder that contains just the input images") # show an "Open" dialog box and return the path to the selected file
# filename = askdirectory(initialdir = ".",title = "Select folder that contains the heatmaps") # show an "Open" dialog box and return the path to the selected file

# test image and heatmap paths
imPath = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\11.jpg'
hmPath = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\heatmaps\n11.jpg'

NORMALIZED = 1./255

# read image
image = cv2.imread(imPath)
heatmap = cv2.imread(hmPath, cv2.IMREAD_GRAYSCALE).astype("float32") * NORMALIZED

# filter image
model.set_input_image(image)
model.set_input_heatmap(heatmap)
model.apply_filters([filters.fade_to_color.FadeToColor()])

# display
cv2.imshow("filtered", model.get_output_image())
# cv2.imshow("test", image)

# wait for user
cv2.waitKey(0)
cv2.destroyAllWindows()
