from tkinter import filedialog


image_filenames = []
heatmap_filenames = []
active_filters = []
save_directory = None

def on_button_pressed_load_image():
    global image_filenames
    image_filenames = filedialog.askopenfilenames(title = "Select the images") # show a file dialog box
    view.preview_image(0)

def on_button_pressed_load_heatmap():
    global heatmap_filenames
    heatmap_filenames = filedialog.askopenfilenames(title = "Select the heatmaps") # show a file dialog box
    view.preview_image(0)

def on_button_pressed_choose_save_location():
    pass

def on_heatmap_adjustments_updated():
    pass

###############################
# update_previews()
#
