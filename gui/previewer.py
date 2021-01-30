import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# image_from_array(some_numpy_array)
def image_from_array(root, cv_image, max_width, max_height):
    # path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    # image = cv2.imread(path)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB) # convert colorspace from BGR to RGB
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

class SingleImagePreviewer(Frame):
    def __init__(self, parent, image_source, source, max_width=None, max_height=None):
        Frame.__init__(self, parent)
        self.label = None
        self.max_width = max_width
        self.max_height = max_height
        self.set(image_source, source)

    def set(self, image_source, source):
        if (source == ImageSource.ARRAY):
            self.image = image_from_array(self, image_source, self.max_width, self.max_height) # save a ref to the image so the garbage collector doesn't delete the image
        elif (source == ImageSource.FILEPATH):
            self.image = image_from_file(self, image_source, self.max_width, self.max_height)
        else:
            raise Exception("Please specify the source, i.e., the format that image is in. (ImageSource.ARRAY, ImageSource.FILEPATH, ...)")

        if (self.label is not None):
            self.label.destroy()
        self.label = Label(self, image=self.image)
        self.label.pack()

class MultiImagePreviewer(Frame):
    def __init__(self, parent, image_sources, source, max_width=None, max_height=None):
        Frame.__init__(self, parent)
        self.image_sources = image_sources
        self.image_frame = SingleImagePreviewer(self, image_sources[0], source, max_width, max_height)
        self.image_frame.pack()
        self.source = source
        self.index = 0
        Button(self, text="Next", command=self.next).pack()

    def next(self):
        self.index = (self.index + 1) % len(self.image_sources)
        self.image_frame.set(self.image_sources[self.index], self.source)

    def show(self, image_index):
        if image_index < len(self.image_sources):
            self.index = image_index
            self.image_frame.set(self.image_sources[self.index], self.source)

    def set(self, image_sources, source):
        self.image_sources = image_sources
        self.source = source
        self.image_frame.set(self.image_sources[0], self.source)

class TabbedImagePreviewer(ttk.Notebook):
    def __init__(self, parent, max_width=None, max_height=None):
        ttk.Notebook.__init__(self, parent)
        self.max_width = max_width
        self.max_height = max_height
        self.tabs = []
        # tab1 = ttk.Frame(self)
        # tab2 = ttk.Frame(self)
        # self.add(tab1, text="All Records")
        # self.add(tab2, text="Add New Record")
        self.pack(expand=1, fill='both')

    def add_multi_image(self, tab_name, image_sources, source):
        f = ttk.Frame(self)
        self.tabs.append(f)
        self.add(f, text=tab_name)
        MultiImagePreviewer(f, image_sources, source, max_width=self.max_width, max_height=self.max_height).pack()

    def add_single_image(self, tab_name, image_source, source):
        f = ttk.Frame(self)
        self.tabs.append(f)
        self.add(f, text=tab_name)
        SingleImagePreviewer(f, image_source, source, max_width=self.max_width, max_height=self.max_height).pack()

if __name__ == "__main__":
    root = Tk()

    path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    path2 = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\05.jpg'
    path3 = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\06.jpg'
    cv2_image = cv2.imread(path)

    tabs = TabbedImagePreviewer(root, max_width="4i", max_height="4i")
    tabs.pack()
    tabs.add_single_image("One lonely image", path, ImageSource.FILEPATH)
    tabs.add_multi_image("Oh wow, two images!", [path2, path3], ImageSource.FILEPATH)

    # MultiImagePreviewer(root, [path, path2, path3], source = ImageSource.FILEPATH, max_width="4i", max_height="4i").pack()

    # SingleImagePreviewer(root, cv2_image, source = ImageSource.ARRAY, max_width="2i", max_height="2i").pack()
    # SingleImagePreviewer(root, image_source=path, source=ImageSource.FILEPATH, max_width="1i", max_height="1i").pack()
    root.mainloop()
