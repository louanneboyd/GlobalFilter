import tkinter as tk
import tkinter.ttk as ttk
import platform

import controller_new as controller
import model
from gui import SingleImagePreviewer, TabbedImagePreviewer, ImageSource, HeatmapAdjustments

from filters import *
# from filters import AccurateBlur, ClassicBlur, Desaturate, FadeToColor, FastBlur

# from gui import HeatmapAdjustments

blank_image_path = r'C:\Users\bmicm\OneDrive\Documents\GitHub\EyeTrackingBlurring\gui\blank.bmp'

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

    def preview_image(self, index):
        if index < len(controller.image_filenames):
            self.__set_preview_input(controller.image_filenames[index])
        if index < len(controller.heatmap_filenames):
            self.__set_preview_heatmap(controller.heatmap_filenames[index])
        if index < len(controller.image_filenames) and index < len(controller.heatmap_filenames):
            self.__set_preview_result(controller.image_filenames[index], controller.heatmap_filenames[index])


    def __set_preview_input(self, filename):
        self.previews.image_input.set(filename, ImageSource.FILEPATH)

    def __set_preview_heatmap(self, filename):
        self.previews.image_heatmap.set(filename, ImageSource.FILEPATH)

    def __update_preview_modified_heatmap():
        pass
        # heatmap_path = controller.heatmap_filenames[controller.preview_index]
        # heatmap = cv2.imread(heatmap_path, cv2.IMREAD_GRAYSCALE).astype("float32") * NORMALIZED
        # model.set_input_heatmap(heatmap)
        # heatmap = (model.get_remapped_heatmap() / NORMALIZED).astype("uint8")
        # preview_heatmap.tabs[1].winfo_children()[0].set(heatmap, ImageSource.ARRAY)

    def __set_preview_result(self, image, heatmap):
        model.run(image, heatmap, controller.active_filters)
        self.previews.image_result.set(model.get_output_image(), ImageSource.ARRAY)

class SaveLoadAndPreviews(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        ttk.Label(self, text="Preview").grid(row=0, column=0, sticky=tk.W)

        ttk.Label(self, text="Images").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text="Heatmaps").grid(row=1, column=1, sticky=tk.W)
        ttk.Label(self, text="Result").grid(row=1, column=2, sticky=tk.W)

        max_size = "2i" # 2 inches

        self.image_input = SingleImagePreviewer(self, image_source=blank_image_path, source=ImageSource.FILEPATH, max_width=max_size, max_height=max_size)
        self.image_input.grid(row=2, column=0, sticky=tk.W)

        # image_heatmap = TabbedImagePreviewer(self)
        self.image_heatmap = SingleImagePreviewer(self, image_source=blank_image_path, source=ImageSource.FILEPATH, max_width=max_size, max_height=max_size)
        self.image_heatmap.grid(row=2, column=1, sticky=tk.W)

        self.image_result = SingleImagePreviewer(self, image_source=blank_image_path, source=ImageSource.FILEPATH, max_width=max_size, max_height=max_size)
        self.image_result.grid(row=2, column=2, sticky=tk.W)


        button_load_image = ttk.Button(self, text="Load", command=controller.on_button_pressed_load_image)
        button_load_image.grid(row=3, column=0, sticky=tk.W)

        button_load_heatmap = ttk.Button(self, text="Load", command=controller.on_button_pressed_load_heatmap)
        button_load_heatmap.grid(row=3, column=1, sticky=tk.W)

        button_choose_save_location = ttk.Button(self, text="Choose Save Location", command=controller.on_button_pressed_choose_save_location)
        button_choose_save_location.grid(row=3, column=2, sticky=tk.W)

        # Previews(self).pack()

class Previews(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        tabs = ttk.Notebook(self)
        tabs.pack(expand=1, fill='both')
        tabs.add(ttk.Frame(tabs), text="Your Images")
        tabs.add(ttk.Frame(tabs), text="Example Image")

class FiltersAndSettings(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")
        # ttk.Label(self, text="Filters").grid(row=0, column=0)
        ttk.Label(self, text="Available Filters   ").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text="Selected Filters   ").grid(row=1, column=2, sticky=tk.W)
        ttk.Label(self, text="Filter Settings   ").grid(row=1, column=3, sticky=tk.W)
        ttk.Label(self, text="Heatmap Adjustments").grid(row=1, column=4, sticky=tk.W)

        AvailableFilters(self).grid(row=2, column=0)
        SwapFilters(self).grid(row=2, column=1)
        ActiveFilters(self).grid(row=2, column=2)
        FilterSettings(self).grid(row=2, column=3)
        HeatmapAdjustments(self, controller.on_heatmap_adjustments_updated).grid(row=2, column=4)

class AvailableFilters(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")

class SwapFilters(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")

class ActiveFilters(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")

class FilterSettings(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness="1p")

if __name__ == "__main__":
    main()
