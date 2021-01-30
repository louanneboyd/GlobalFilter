import numpy as np
from tkinter import *

def map_smoothstep(data):
    return data * data * (3 - 2 * data);

def map_ease_in_quadratic(data):
    return data * data

def map_ease_out_quadratic(data):
    return 1 - (1 - data) * (1 - data)  # invert, square it, and invert again

def map_ease_inout_quadratic(data):
    return ( 2 * data * data ) if ( data < 0.5 ) else ( 1 - (2 * (1-data) * (1-data)) )

class GUI_HeatmapAdjustments(Frame):
    def __init__(self, parent, callback):
        Frame.__init__(self, parent)

        self.callback = callback
        self.curve = StringVar()
        self.curve.set("Linear")

        preview = Frame(self)
        settings = Frame(self)
        preview.pack()
        settings.pack()

        # Label(settings, text="Clamp").grid(row=0, column=0, sticky=W)
        # Checkbutton(settings, variable=None).grid(row=0, column=1, sticky=W)

        # Label(settings, text="Curve").grid(row=1, column=0, sticky=W)
        # OptionMenu(settings, None, "Linear", "Ease In (Quadratic)", "Ease Out (Quadratic)", "Ease In/Out (Quadratic)", "Smoothstep").grid(row=1, column=1, sticky=W)

        Label(settings, text="Minimum").grid(row=2, column=0, sticky=W)
        frame_min = Frame(settings)
        frame_min.grid(row=3, column=0, columnspan=2, sticky=W)
        Label(frame_min, text="    From").pack(side=LEFT)
        Label(frame_min, text="0.0").pack(side=LEFT)
        Label(frame_min, text="To").pack(side=LEFT)
        entry_min = Entry(frame_min)
        entry_min.pack(side=LEFT)
        entry_min.insert(0, "0.0")

        Label(settings, text="Maximum").grid(row=4, column=0, sticky=W)
        frame_max = Frame(settings)
        frame_max.grid(row=5, column=0, columnspan=2, sticky=W)
        Label(frame_max, text="    From").pack(side=LEFT)
        Label(frame_max, text="1.0").pack(side=LEFT)
        Label(frame_max, text="To").pack(side=LEFT)
        entry_max = Entry(frame_max)
        entry_max.pack(side=LEFT)
        entry_max.insert(0, "1.0")

        self.get_min_value = lambda: float(entry_min.get())
        self.get_max_value = lambda: float(entry_max.get())

        Button(settings, text="Update", command=lambda:callback(self.get_values())).grid(row=6, columnspan=2)

    def get_values(self):
        return {
        "min": self.get_min_value(),
        "max": self.get_max_value(),
        # "curve": self.curve.get(),
        }

if __name__ == "__main__":
    root = Tk()
    GUI_HeatmapAdjustments(root, lambda values:print(values)).pack()
    root.mainloop()
