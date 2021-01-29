import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# image_from_array(some_numpy_array)
def image_from_array(root, cv_image, max_width, max_height):
    # path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    # image = cv2.imread(path)
    pil_image = Image.fromarray(cv_image)
    resize_pil_image(root, pil_image, max_width, max_height)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

# image_from_file(filepath, width, height)
def image_from_file(root, uri, max_width, max_height):
    pil_image = Image.open(uri)
    resize_pil_image(root, pil_image, max_width, max_height)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

def resize_pil_image(root, image, max_width, max_height):
    if (max_width is not None and max_height is not None): # change the image size to fit in a thumbnail
        max_width = int(root.winfo_fpixels(max_width)) # convert the max_width to device pixels from physical units
        max_height = int(root.winfo_fpixels(max_height)) # convert the max_height to device pixels from physical units
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)

def example_image(root, dimensions = None):
    path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    return image_from_file(root, path, dimensions)

class ImageSource():
    ARRAY = 0
    FILEPATH = 1

class GUI_SingleImagePreviewer(Frame):
    def __init__(self, parent, image_source, data_type, max_width=None, max_height=None):
        Frame.__init__(self, parent)
        self.label = None
        self.max_width = max_width
        self.max_height = max_height
        self.set(image_source, data_type)

    def set(self, image_source, data_type):
        if (data_type == ImageSource.ARRAY):
            self.image = image_from_array(self, image_source, self.max_width, self.max_height) # save a ref to the image so the garbage collector doesn't delete the image
        elif (data_type == ImageSource.FILEPATH):
            self.image = image_from_file(self, image_source, self.max_width, self.max_height)
        else:
            raise Exception("Please specify the data_type, i.e., the format that image is in. (ImageSource.ARRAY, ImageSource.FILEPATH, ...)")

        if (self.label is not None):
            self.label.destroy()
        self.label = Label(self, image=self.image)
        self.label.pack()

class GUI_MultiImagePreviewer(Frame):
    def __init__(self, parent, image_sources, data_type, max_width=None, max_height=None):
        Frame.__init__(self, parent)
        self.image_sources = image_sources
        self.image_frame = GUI_SingleImagePreviewer(self, image_sources[0], data_type, max_width, max_height)
        self.image_frame.pack()
        self.data_type = data_type
        self.index = 0
        Button(self, text="Next", command=self.next).pack()

    def next(self):
        self.index = (self.index + 1) % len(self.image_sources)
        self.image_frame.set(self.image_sources[self.index], self.data_type)

    def show(self, image_index):
        if image_index < len(self.image_sources):
            self.index = image_index
            self.image_frame.set(self.image_sources[self.index], self.data_type)

    def set(self, image_sources, data_type):
        self.image_sources = image_sources
        self.data_type = data_type
        self.image_frame.set(self.image_sources[0], self.data_type)

class GUI_TabbedImagePreviewer(ttk.Notebook):
    def __init__(self, parent, max_width=None, max_height=None):
        ttk.Notebook.__init__(self, parent)
        self.max_width = max_width
        self.max_height = max_height
        self.tabs = []
        tab1 = ttk.Frame(self)
        tab2 = ttk.Frame(self)
        self.add(tab1, text="All Records")
        self.add(tab2, text="Add New Record")
        self.pack(expand=1, fill='both')

    def add_single_image(image_sources, data_type):
        f = ttk.Frame(self)
        self.tabs.append(f)
        GUI_MultiImagePreviewer(f, image_sources, data_type)

    def add_multi_image(image_source, data_type):
        f = ttk.Frame(self)
        self.tabs.append(f)
        GUI_SingleImagePreviewer(f, image_source, data_type)

if __name__ == "__main__":
    root = Tk()

    path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    path2 = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\05.jpg'
    path3 = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\06.jpg'
    cv2_image = cv2.imread(path)

    GUI_TabbedImagePreviewer(root).pack()

    # GUI_MultiImagePreviewer(root, [path, path2, path3], data_type = ImageSource.FILEPATH, max_width="4i", max_height="4i").pack()

    # GUI_SingleImagePreviewer(root, cv2_image, data_type = ImageSource.ARRAY, max_width="2i", max_height="2i").pack()
    # GUI_SingleImagePreviewer(root, image_source=path, data_type=ImageSource.FILEPATH, max_width="1i", max_height="1i").pack()
    # GUI_SingleImagePreviewer(root).pack()
    root.mainloop()
