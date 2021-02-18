import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import platform
import cv2
import numpy as np

import controller
import model
from gui import SingleImagePreviewer, TabbedImagePreviewer, ImageSource, HeatmapAdjustments
from filters.helpers import attributes as attr

blank_image = np.zeros((1,1,3), np.uint8)
observers_to_refresh = [] # (observer design pattern) a list of the functions to call whenever refresh_settings() is called

def change_state_of_all_widgets(root, state): # states: tk.ENABLED, tk.DISABLED, tk.NORMAL
    if "state" in root.config():
        root["state"] = state
    for child in root.winfo_children():
        change_state_of_all_widgets(child, state)

def rgb_to_hex(rgb):
    r, g, b = (int(i) for i in rgb) # convert from floats to ints
    return "#%02x%02x%02x" % (r,g,b)

def main():
    # hidpi support on windows
    if (platform.system() == "Windows"):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # initialize gui
    root = tk.Tk()
    root.winfo_toplevel().title("Global Filter")
    controller.view = View(root)
    controller.view.pack()
    root.mainloop()

#############################
# View
# The whole gui of the program
#
class View(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.previews = SaveLoadAndPreviews(self)
        self.previews.pack()

        self.settings = FiltersAndSettings(self)
        self.settings.pack()

        # allow direct access to the tk.messagebox
        self.messagebox = tk.messagebox

        # reload preview images whenever view.refresh is called
        observers_to_refresh.append(lambda: self.preview_image(0))

    def get_selected_available_filter_index(self):
        return self.settings.available.selected_filter_from_available.get()

    def get_selected_active_filter_index(self):
        return self.settings.active.selected_filter_from_active.get()

    def set_selected_active_filter_index(self, index):
        self.settings.active.selected_filter_from_active.set(index)
        self.settings.active.filter_settings_frame.populate(index)

    def get_selected_active_filter(self):
        if len(controller.active_filters) > 0:
            return controller.active_filters[self.get_selected_active_filter_index()]
        else:
            return None

    def preview_image(self, index):
        if index < len(controller.image_filenames):
            self.__set_preview_input(controller.image_filenames[index])
        if index < len(controller.heatmap_filenames):
            self.__set_preview_heatmap(controller.heatmap_filenames[index])
            self.__update_preview_modified_heatmap(controller.heatmap_filenames[index])
        if index < len(controller.image_filenames) and index < len(controller.heatmap_filenames):
            self.__set_preview_result(controller.image_filenames[index], controller.heatmap_filenames[index])

    def __set_preview_input(self, filename):
        self.previews.image_input.set(filename, ImageSource.FILEPATH)

    def __set_preview_heatmap(self, filename):
        self.previews.image_heatmap.set(filename, ImageSource.FILEPATH)

    def __update_preview_modified_heatmap(self, filename):
        heatmap = cv2.imread(filename, cv2.IMREAD_GRAYSCALE).astype("float32") * model.NORMALIZED
        model.set_input_heatmap(heatmap)
        heatmap = (model.get_remapped_heatmap() / model.NORMALIZED).astype("uint8")
        self.previews.image_heatmap_adjusted.set(heatmap, ImageSource.ARRAY)

    def __set_preview_result(self, image, heatmap):
        model.run(image, heatmap, controller.active_filters)
        self.previews.image_result.set(model.get_output_image(), ImageSource.ARRAY)

    def refresh(self):
        for func in observers_to_refresh:
            func()

    def change_state(self, state):
        change_state_of_all_widgets(self, state)


class SaveLoadAndPreviews(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        self.parent = parent
        ttk.Label(self, text="Preview").grid(row=0, column=0, sticky=tk.W)

        ttk.Label(self, text="Images   ").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text="Heatmaps (original)   ").grid(row=1, column=1, sticky=tk.W)
        ttk.Label(self, text="(adjusted)   ").grid(row=1, column=2, sticky=tk.W)
        ttk.Label(self, text="Result").grid(row=1, column=3, sticky=tk.W)

        max_size = "2i" # 2 inches

        self.image_input = SingleImagePreviewer(self, image_source=blank_image, source=ImageSource.ARRAY, max_width=max_size, max_height=max_size)
        self.image_input.grid(row=2, column=0, sticky=tk.W)

        # image_heatmap = TabbedImagePreviewer(self)
        self.image_heatmap = SingleImagePreviewer(self, image_source=blank_image, source=ImageSource.ARRAY, max_width=max_size, max_height=max_size)
        self.image_heatmap.grid(row=2, column=1, sticky=tk.W)

        self.image_heatmap_adjusted = SingleImagePreviewer(self, image_source=blank_image, source=ImageSource.ARRAY, max_width=max_size, max_height=max_size)
        self.image_heatmap_adjusted.grid(row=2, column=2, sticky=tk.W)

        self.image_result = SingleImagePreviewer(self, image_source=blank_image, source=ImageSource.ARRAY, max_width=max_size, max_height=max_size)
        self.image_result.grid(row=2, column=3, sticky=tk.W)


        button_load_image = ttk.Button(self, text="Load Images", command=controller.on_button_pressed_load_image)
        button_load_image.grid(row=3, column=0, sticky=tk.W)

        button_load_heatmap = ttk.Button(self, text="Load Heatmaps", command=controller.on_button_pressed_load_heatmap)
        button_load_heatmap.grid(row=3, column=1, sticky=tk.W)

        button_choose_save_location = ttk.Button(self, text="Choose Save Location", command=controller.on_button_pressed_choose_save_location)
        button_choose_save_location.grid(row=3, column=3, sticky=tk.W)

        ttk.Button(self, text="Refresh Preview", command=lambda: self.parent.preview_image(0)).grid(row=1, column=4, rowspan = 3)


class FiltersAndSettings(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        # ttk.Label(self, text="Filters").grid(row=0, column=0)
        ttk.Label(self, text="Available Filters   ").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text="<--->").grid(row=1, column=1)
        ttk.Label(self, text="Active Filters   ").grid(row=1, column=2, sticky=tk.W)
        ttk.Label(self, text="Filter Settings   ").grid(row=1, column=3, sticky=tk.W)
        ttk.Label(self, text="Heatmap Adjustments").grid(row=1, column=4, sticky=tk.W)

        self.available = AvailableFilters(self)
        self.available.grid(row=2, column=0, sticky=tk.N)
        SwapFilters(self).grid(row=2, column=1, sticky=tk.N)
        fs = FilterSettings(self)
        fs.grid(row=2, column=3, sticky=tk.N)
        self.active = ActiveFilters(self, fs)
        self.active.grid(row=2, column=2, sticky=tk.N)
        HeatmapAdjustments(self, controller.on_heatmap_adjustments_updated).grid(row=2, column=4, sticky=tk.N)
        RunButton(self).grid(row=3, column=5, sticky=tk.W)

class AvailableFilters(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        self.selected_filter_from_available = tk.IntVar()
        for i, filter in enumerate(controller.available_filters):
            tk.Radiobutton(self, text=filter.name, value=i, variable=self.selected_filter_from_available, indicator = 0, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

class SwapFilters(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        ttk.Button(self, text="Add", command = controller.on_button_pressed_filter_add).pack(fill=tk.X)
        ttk.Button(self, text="Remove", command = controller.on_button_pressed_filter_remove).pack(fill=tk.X)
        ttk.Button(self, text="Remove  All", command = controller.on_button_pressed_filter_remove_all).pack(fill=tk.X)
        ttk.Button(self, text="▲", command = controller.on_button_pressed_filter_move_up).pack(fill=tk.X)
        ttk.Button(self, text="▼", command = controller.on_button_pressed_filter_move_down).pack(fill=tk.X)

class ActiveFilters(ttk.Frame):
    def __init__(self, parent, filter_settings_frame):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        self.filter_settings_frame = filter_settings_frame
        self.selected_filter_from_active = tk.IntVar()
        observers_to_refresh.append(self.refresh)

    def refresh(self): # make sure that the visible list of active filters is up to date
        for child in self.winfo_children():
            child.destroy()
        for i, filter in enumerate(controller.active_filters):
            tk.Radiobutton(self, text=filter.name, value=i, variable=self.selected_filter_from_active, indicator = 0, command=lambda: self.filter_settings_frame.populate(self.selected_filter_from_active.get()), anchor=tk.W).pack(side=tk.TOP, fill=tk.X)
            # tk.Radiobutton(self, text=i, value=i, variable=self.selected_filter_from_active, indicator = 0, command=lambda: print(self.selected_filter_from_active.get()), anchor=tk.W).pack(side=tk.TOP, fill=tk.X)

class FilterSettings(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)#, highlightbackground="black", highlightthickness="1p")

    def populate(self, filter_id):
        if filter_id >= len(controller.active_filters):
            return

        if len(controller.active_filters) == 0:
            filter = None
            return

        filter = controller.active_filters[filter_id]

        for child in self.winfo_children():
            child.destroy()

        if filter_id < 0:
            return

        for i, name in enumerate(filter.attributes):
            attr = filter.attributes[name]
            display = get_attribute_display(self, attr)
            if display is not None:
                ttk.Label(self, text=name + " ").grid(row=i, column=0, sticky=tk.E)
                display.grid(row=i, column=1)


def get_attribute_display(parent, attribute):
    if isinstance(attribute, attr.RGBColorPickerAttribute):
        return RGBColorPicker(parent, attribute)
    if (isinstance(attribute, attr.SliderAttribute)):
        return Slider(parent, attribute)
    if (isinstance(attribute, attr.TextEntryAttribute)):
        return TextEntry(parent, attribute)

class Slider(ttk.Frame):
    def __init__(self, parent, attribute):
        tk.Frame.__init__(self, parent)
        entry_value = tk.IntVar()
        entry_value.set(attribute.value)
        e = ttk.Entry(self, textvariable=entry_value)
        e.pack(side=tk.LEFT)
        tk.Button(self, text="Update", command=lambda:self.update_value(attribute, entry_value)).pack(side=tk.LEFT)

    def update_value(self, attribute, value_from_tk_entry):
        v = value_from_tk_entry.get()
        v = min(v, attribute.max)
        v = max(v, attribute.min)
        value_from_tk_entry.set(v)
        attribute.value = v
        controller.view.refresh()

class TextEntry(ttk.Frame):
    def __init__(self, parent, attribute):
        pass

class RGBColorPicker(ttk.Frame):
    def __init__(self, parent, attribute):
        tk.Frame.__init__(self, parent)
        self.attribute = attribute
        # ttk.Label(self, text="Color ").pack(side=tk.LEFT)
        rgb = attribute.value
        self.preview = tk.Button(self, text="     ", bg=rgb_to_hex(rgb), command=self.set_color)
        self.preview.pack(side=tk.LEFT)
        tk.Button(self, text="(Choose)", command=self.set_color).pack()

    def set_color(self):
        rgb, hex = colorchooser.askcolor()
        self.preview["bg"] = hex
        self.attribute.value = rgb
        controller.view.refresh()

class RunButton(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Button(self, text="▶ Run", bg="green", command=controller.on_button_pressed_run).pack()

if __name__ == "__main__":
    main()
