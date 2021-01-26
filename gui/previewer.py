import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# image_from_array(some_numpy_array)
def image_from_array(cv_image, max_width, max_height):
    # path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    # image = cv2.imread(path)
    pil_image = Image.fromarray(cv_image)
    resize_pil_image(pil_image, max_width, max_height)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

# image_from_file(filepath, width, height)
def image_from_file(uri, max_width, max_height):
    pil_image = Image.open(uri)
    resize_pil_image(pil_image, max_width, max_height)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

def resize_pil_image(image, max_width, max_height):
    if (max_width is not None and max_height is not None): # change the image size to fit in a thumbnail
        max_width = int(root.winfo_fpixels(max_width)) # convert the max_width to device pixels from physical units
        max_height = int(root.winfo_fpixels(max_height)) # convert the max_height to device pixels from physical units
        print(max_width, max_height)
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)

def example_image(dimensions = None):
    path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    return image_from_file(path, dimensions)

class GUI_MultiImagePreviewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        label = Label(self, text="Hello, world")
        label.pack()

# class GUI_SingleImage(Frame):
#     def __init__(self, parent, max_width=None, max_height=None, numpy_image=None, filepath=None):
#         Frame.__init__(self, parent)
#         self.label = None
#         self.set(max_width, max_height, numpy_image, filepath)
#
#     def set(self, max_width=None, max_height=None, numpy_image=None, filepath=None):
#         if (numpy_image is not None):
#             self.image = image_from_array(numpy_image, max_width, max_height) # save a ref to the image so the garbage collector doesn't delete the image
#         elif (filepath is not None):
#             self.image = image_from_file(filepath, max_width, max_height)
#         else:
#             raise Exception("No source image has been specified. Please specify either `numpy_image` or `filepath` as an argument")
#
#         if (self.label is not None):
#             self.label.destroy()
#         self.label = Label(self, image=self.image)
#         self.label.pack()

root = Tk()

path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
cv2_image = cv2.imread(path)

GUI_MultiImagePreviewer(root)

# GUI_SingleImage(root, numpy_image=cv2_image, max_width="2i", max_height="2i").pack()
# GUI_SingleImage(root, filepath=path, max_width="1i", max_height="1i").pack()
# GUI_SingleImage(root).pack()
root.mainloop()
