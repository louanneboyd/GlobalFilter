# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:06:46 2020

@author: bmicm
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Select folder of source images
        self.photos_dir = tk.Label(self, text = "Folder of Source Images")
        self.photos_dir_entry = tk.Entry(self, text = "" )
        self.photos_dir_load = tk.Button(self, text="Choose...", command=self.browse_photos)

        self.photos_dir.grid(       column=0, row=0)
        self.photos_dir_entry.grid( column=0, row=1)
        self.photos_dir_load.grid(  column=0, row=2)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).grid(column=1, row=0, rowspan = 3, sticky="ns")

        # Select folder of source heatmaps
        self.heatmaps_dir = tk.Label(self, text = "Folder of Source Heatmaps")
        self.heatmaps_dir_entry = tk.Entry(self, text = "" )
        self.heatmaps_dir_load = tk.Button(self, text="Choose...", command=self.browse_heatmaps)

        self.heatmaps_dir.grid(       column=2, row=0)
        self.heatmaps_dir_entry.grid( column=2, row=1)
        self.heatmaps_dir_load.grid(  column=2, row=2)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).grid(column=3, row=0, rowspan = 3, sticky="ns")

        # Select folder of output
        self.output_dir = tk.Label(self, text = "Output Folder")
        self.output_dir_entry = tk.Entry(self, text = "" )
        self.output_dir_load = tk.Button(self, text="Choose...", command=self.browse_output)

        self.output_dir.grid(       column=4, row=0)
        self.output_dir_entry.grid( column=4, row=1)
        self.output_dir_load.grid(  column=4, row=2)

        # Separator
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(column=0, row=3, columnspan = 10, sticky="ew")

        # Filters
        self.filter_list = tk.Label(self, text = "Filters")
        for i in range(3):
            self.check = tk.Checkbutton(self, text=f"Filter{i}")
            self.check.grid(column=0, row=5+i)

        self.filter_list.grid(column=0, row=4)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).grid(column=1, row=4, rowspan = 4, sticky="ns")

        # Curve
        self.curve = tk.Label(self, text = "Interpolation")
        # @TODO Insert drawing of the current curve
        self.curve_name = tk.Label(self, text="(Default) Linear")
        self.curve_select = tk.Button(self, text="Choose...", command=self.new_window)

        self.curve.grid(column=2, row=4)
        self.curve_name.grid(column=2, row=5)
        self.curve_select.grid(column=2, row=6)

        # Separator
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(column=0, row=8, columnspan = 10, sticky="ew")

        # Quit button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(column=2, row=20)

    def say_hi(self):
        print("hi there, everyone!")

    def new_window(self):
        window = tk.Toplevel(root)

    def browse_photos(self):
        folder = filedialog.askdirectory(title='Locate where the source images are held')
        self.photos_dir_entry.insert(0, folder)

    def browse_heatmaps(self):
        folder = filedialog.askdirectory(title='Locate where the source heatmaps are held')
        self.heatmaps_dir_entry.insert(0, folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title='Choose where to save the filtered photos')
        self.output_dir_entry.insert(0, folder)

root = tk.Tk()
root.tk.call('tk', 'scaling', 4.0)
app = Application(master=root)
app.mainloop()
