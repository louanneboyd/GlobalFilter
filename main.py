import cv2
from tkinter import Tk
from tkinter import filedialog

import model
import filters.desaturate
import filters.fade_to_color
import filters.fast_blur
import filters.accurate_blur

def test_images_from_explorer(filters):
    # Ask the user for the image folder and the heatmap folder
    Tk().withdraw()
    image_filenames = filedialog.askopenfilenames(initialdir = ".", title = "Select the input images") # show an "Open" dialog box and return the path to the selected file
    heatmap_filenames = filedialog.askopenfilenames(initialdir = ".",title = "Select the input heatmaps") # show an "Open" dialog box and return the path to the selected file

    if len(image_filenames) != len(heatmap_filenames):
        print("Error: The number of selected images doesn't match the number of selected heatmaps.")
        return

    for i in range(len(image_filenames)):
        test_run(image_filenames[i], heatmap_filenames[i], filters)

def test_single_image(filters):
    # test image and heatmap paths
    imPath = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\13.jpg'
    hmPath = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\heatmaps\n13.jpg'

    test_run(imPath, hmPath, filters)

def test_run(image_path, heatmap_path, filters):
    NORMALIZED = 1./255

    # read image
    image = cv2.imread(image_path)
    heatmap = cv2.imread(heatmap_path, cv2.IMREAD_GRAYSCALE).astype("float32") * NORMALIZED

    # filter image
    model.set_input_image(image)
    model.set_input_heatmap(heatmap)
    model.apply_filters(filters)

    # display
    cv2.imshow("filtered", model.get_output_image())
    # cv2.imshow("test", image)

    # wait for user
    cv2.waitKey(0)

######################################################################

filters_to_run = [
    # filters.fade_to_color.FadeToColor(),
    # filters.desaturate.Desaturate(),
    filters.fast_blur.FastBlur(),
    # filters.accurate_blur.AccurateBlur(),
    ]

# test_images_from_explorer(filters_to_run)
test_single_image(filters_to_run)

cv2.destroyAllWindows()
