from tkinter import filedialog

import model
from available_filters import available_filters

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

def on_heatmap_adjustments_updated(data):
    model.heatmap_remapping_data = data
    view.refresh()

def on_button_pressed_filter_add():
    filter = available_filters[view.get_selected_filter_index_from_available()]
    active_filters.append(filter())
    view.refresh()

def on_button_pressed_filter_remove():
    pass

def on_button_pressed_filter_remove_all():
    active_filters.clear()
    view.refresh()

def on_button_pressed_filter_move_up():
    pass

def on_button_pressed_filter_move_down():
    pass
