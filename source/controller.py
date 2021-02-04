import cv2
from os.path import split
from tkinter import filedialog

from available_filters import available_filters
import model

image_filenames = []
heatmap_filenames = []
active_filters = []
save_directory = None


def on_button_pressed_load_image():
    global image_filenames
    new_filenames = filedialog.askopenfilenames(title = "Select the images") # show a file dialog box
    if (new_filenames != ''): # only update list of filenames if there were any filenames actually selected
        image_filenames = new_filenames
    view.preview_image(0)

def on_button_pressed_load_heatmap():
    global heatmap_filenames
    new_filenames = filedialog.askopenfilenames(title = "Select the heatmaps") # show a file dialog box
    if (new_filenames != ''): # only update list of filenames if there were any filenames actually selected
        heatmap_filenames = new_filenames
    view.preview_image(0)

def on_button_pressed_choose_save_location():
    global save_directory
    new_dir = filedialog.askdirectory(title = "Select where the generated images will be saved")
    if (new_dir != ''): # only update folder if there was a folder actually selected
        save_directory = new_dir

def on_heatmap_adjustments_updated(data):
    model.heatmap_remapping_data = data
    view.refresh()

def on_button_pressed_filter_add():
    filter = available_filters[view.get_selected_available_filter_index()]
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

def on_button_pressed_run():
    print(len(image_filenames))

    # Fatal user mistakes (the filter won't run without these)
    if not image_filenames:
        view.messagebox.showwarning(title="Missing Images", message="Before running the filter, please click \"Load Images\" and select the images on which to run the filter")
        return
    if not heatmap_filenames:
        view.messagebox.showwarning(title="Missing Heatmaps", message="Before running the filter, please click \"Load Heatmaps\" and select the heatmaps on which to run the filter")
        return
    if len(image_filenames) < len(heatmap_filenames):
        view.messagebox.showwarning(title="Input Mismatch: Too Many Heatmaps; Not Enough Images", message=f"You've selected {len(image_filenames)} image(s) and {len(heatmap_filenames)} heatmap(s). There should be exactly one heatmap per image. \nPlease check that you have selected all of the files that you need.")
        return
    if len(image_filenames) > len(heatmap_filenames):
        view.messagebox.showwarning(title="Input Mismatch: Too Many Images; Not Enough Heatmaps", message=f"You've selected {len(image_filenames)} image(s) and {len(heatmap_filenames)} heatmap(s). There should be exactly one heatmap per image. \nPlease check that you have selected all of the files that you need.")
        return
    if not save_directory:
        view.messagebox.showwarning(title="Missing Save Location", message="Before running the filter, please click \"Choose Save Location\" and select a folder for the newly generated images to be saved to.")
        return

    # Possible user mistakes (the user may have made a mistake, or may be intending this behavior)
    if not active_filters:
        is_ok = view.messagebox.askokcancel(title="No Filters Were Selected", message="No Filters Were Selected. The generated images will be the same as the input images.\nIf this is intentional, please press \"ok\" to continue.")
        if not is_ok:
            return

    # Finally, run the filter on all of the files
    view.change_state("disabled")
    for i in range(len(image_filenames)):
        model.run(image_filenames[i], heatmap_filenames[i], active_filters)
        filename_without_path = split(image_filenames[i])[1]
        path = save_directory + "/" + filename_without_path
        cv2.imwrite(filename = path, img = model.get_output_image())
        # # display
        # imshow("filtered", model.get_output_image())
        # waitKey(0) # wait for user input to show next image
    count = len(image_filenames)
    view.messagebox.showinfo(title="Filter complete!", message=str(count) + (" images have " if count != 1 else " image has ") + "been generated and saved to the folder:\n" + save_directory)
    view.change_state("normal")
