import cv2
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import platform
from PIL import Image, ImageTk

import filters.desaturate
import filters.fade_to_color
import filters.fast_blur
import filters.accurate_blur
import model

from gui import GUI_SingleImagePreviewer
from gui import GUI_MultiImagePreviewer
from gui import GUI_HeatmapAdjustments
from gui import ImageSource

available_filters = [
    filters.accurate_blur.AccurateBlur,
    filters.fast_blur.FastBlur,
    filters.desaturate.Desaturate,
    filters.fade_to_color.FadeToColor,
]

active_filters = []

image_filenames = []
heatmap_filenames = []

input_image_frame = None
input_heatmap_frame = None
output_frame = None

preview_index = 0
preview_heatmap = None
heatmap_remapping_data = {}

NORMALIZED = 1./255

def make_image_label(gui_parent, image):
    image = ImageTk.PhotoImage(Image.fromarray(image)) # convert to tk's image format
    label = Label(gui_parent, image=image)
    label.image = image
    return label

def add_filter(frame):
    selected = available_filters[selected_filter_from_available.get()]
    global active_filters
    active_filters.append( selected() )
    Radiobutton(frame, text=selected.name, value=len(active_filters) - 1, variable=selected_filter_from_active, indicator = 0, anchor=W).pack(side=BOTTOM, fill=X)
    update_previews()

# @TODO make remove_filter remove just one filter, rather than all filters
def remove_filter(frame):
    global active_filters
    active_filters = []
    for child in frame.winfo_children():
        child.destroy()

def remove_all_filters(frame):
    global active_filters
    active_filters = []
    for child in frame.winfo_children():
        child.destroy()

def update_heatmap(data):
    global preview_heatmap
    global heatmap_remapping_data
    if (preview_heatmap is not None):
        model.remap_heatmap(data)
        preview_heatmap = model.remapped_heatmap

def run(image_path, heatmap_path, filters):

    # read image
    image = cv2.imread(image_path)
    heatmap = cv2.imread(heatmap_path, cv2.IMREAD_GRAYSCALE).astype("float32") * NORMALIZED

    # filter image
    model.set_input_image(image)
    model.set_input_heatmap(heatmap)
    model.apply_filters(filters)

def run_all():
    print(len(image_filenames))
    for i in range(len(image_filenames)):
        print(i)
        run(image_filenames[i], heatmap_filenames[i], active_filters)
        # display
        cv2.imshow("filtered", model.get_output_image())

        # wait for user
        cv2.waitKey(0)

def update_previews():
    # update preview of the input images
    if (image_filenames is not None and preview_index < len(image_filenames)):
        preview_input_image.set(image_filenames[preview_index], ImageSource.FILEPATH)

    # update preview of the input heatmaps
    if (heatmap_filenames is not None and preview_index < len(heatmap_filenames)):
        preview_heatmap.set(heatmap_filenames[preview_index], ImageSource.FILEPATH)

    # update preview of the output images
    if (len(image_filenames) > preview_index and len(heatmap_filenames) > preview_index):
        run(image_filenames[preview_index], heatmap_filenames[preview_index], active_filters)
        preview_output.set(model.get_output_image(), ImageSource.ARRAY)

def load_images():
    global image_filenames
    global preview_index
    preview_index = 0
    # show an file dialog box and return the path to the selected file
    image_filenames = filedialog.askopenfilenames(title = "Select the input images")
    update_previews()


def load_heatmaps():
    global heatmap_filenames
    # show an file dialog box and return the path to the selected file
    heatmap_filenames = filedialog.askopenfilenames(title = "Select the input heatmaps")
    update_previews()

def main():
    # hidpi support on windows
    if (platform.system() == "Windows"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Test image
    path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\images\04.jpg'
    hmpath = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\data\first 50 images\input\heatmaps\n04.jpg'
    image = cv2.imread(path)

    gui = Tk()
    gui.winfo_toplevel().title("Global Filter")

    top = Frame(gui)
    bottom = Frame(gui)
    top.pack()
    ttk.Separator(gui,orient=HORIZONTAL).pack(side=BOTTOM)
    bottom.pack(side=BOTTOM)

    global selected_filter_from_available
    selected_filter_from_available = IntVar()
    global selected_filter_from_active
    selected_filter_from_active = IntVar()

    ################ top row (image previews) ################
    Label(top, text="Images").grid(row=0, column=0, sticky=W)
    global input_image_frame
    input_image_frame = Frame(top, highlightbackground="black", highlightthickness="1p")
    input_image_frame.grid(row=1, column=0)
    image_size = "2i"
    global preview_input_image
    preview_input_image = GUI_SingleImagePreviewer(input_image_frame, path, data_type = ImageSource.FILEPATH, max_width=image_size, max_height=image_size)
    preview_input_image.pack(side=LEFT, padx=10, pady=10)
    # GUI_SingleImagePreviewer(input_image_frame, image_source=path, data_type=ImageSource.FILEPATH, max_width=image_size, max_height=image_size).pack(side=LEFT, padx=10, pady=10)
    Button(top, text="Load", command=load_images).grid(row=2, column=0, sticky=W)

    Label(top, text="Heatmaps").grid(row=0, column=1, sticky=W)
    input_heatmap_frame = Frame(top, highlightbackground="black", highlightthickness="1p")
    input_heatmap_frame.grid(row=1, column=1)
    global preview_heatmap
    preview_heatmap = GUI_SingleImagePreviewer(input_heatmap_frame, image_source=hmpath, data_type=ImageSource.FILEPATH, max_width=image_size, max_height=image_size)
    preview_heatmap.pack(side=LEFT, padx=10, pady=10)
    Button(top, text="Load", command=load_heatmaps).grid(row=2, column=1, sticky=W)

    Label(top, text="Result (Preview)").grid(row=0, column=3, sticky=W)
    output_frame = Frame(top, highlightbackground="black", highlightthickness="1p")
    output_frame.grid(row=1, column=3)
    global preview_output
    preview_output = GUI_SingleImagePreviewer(output_frame, image_source=path, data_type=ImageSource.FILEPATH, max_width=image_size, max_height=image_size)
    preview_output.pack(side=LEFT, padx=10, pady=10)
    Button(top, text="Choose Save Location...").grid(row=2, column=3, sticky=W)

    ################ bottom row (filter & heatmap options) ################

    ##################
    ### available filters
    Label(bottom, text="Available Filters").grid(row=0, column=0, sticky=W)
    frame = Frame(bottom, highlightbackground="black", highlightthickness="1p")
    frame.grid(row=1, column=0)
    for i, filter in enumerate(available_filters):
        Radiobutton(frame, text=filter.name, value=i, variable=selected_filter_from_available, indicator = 0, anchor=W).pack(side=BOTTOM, fill=X)

    ##################
    ### active filters
    Label(bottom, text="Selected Filters").grid(row=0, column=2, sticky=W)
    active_filters_frame = Frame(bottom, highlightbackground="black", highlightthickness="1p")
    active_filters_frame.grid(row=1, column=2)

    ##################
    ### buttons for filter adding & ordering
    frame = Frame(bottom)
    frame.grid(row=1, column=1)
    Button(frame, text="Add", command = lambda: add_filter(active_filters_frame)).pack(fill=X)
    Button(frame, text="Remove", command = lambda: remove_filter(active_filters_frame)).pack(fill=X)
    Button(frame, text="Remove  All", command = lambda: remove_all_filters(active_filters_frame)).pack(fill=X)
    Button(frame, text="▲").pack(fill=X)
    Button(frame, text="▼").pack(fill=X)

    ##################
    ### settings for the selected active filter
    Label(bottom, text="Filter Settings").grid(row=0, column=3, sticky=W)
    # frame = Frame(bottom, highlightbackground="black", highlightthickness="1p")
    # frame.grid(row=1, column=3)

    ##################
    ### heatmap adjustments
    Label(bottom, text="Heatmap Adjustments").grid(row=0, column=4, sticky=W)
    frame = Frame(bottom, highlightbackground="black", highlightthickness="1p")
    frame.grid(row=1, column=4)
    GUI_HeatmapAdjustments(frame, update_heatmap).pack()

    ##################
    ### run
    Button(bottom, text="▶ Run", bg="green", command=run_all).grid(row=0, column=5, sticky=W)

    gui.mainloop()

main()
