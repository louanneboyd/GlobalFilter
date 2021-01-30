import numpy as np

__image = None
__heatmap = None
heatmap_remapping_data = None

def set_input_image(image):
    global __image
    __image = image

def set_input_heatmap(heatmap):
    global __heatmap
    __heatmap = heatmap

def get_remapped_heatmap():
    if (heatmap_remapping_data is None):
        return __heatmap
    else:
        return map_range(__heatmap, 0, 1, heatmap_remapping_data["min"], heatmap_remapping_data["max"], True)
    # data["curve"]

###
# map_range:
# for a set of data that spans the range a1 to a1,
# remap the data to span the range b1 to b2.
# for example, a heatmap may be brighted by remapping it from 0 - 1 to 0.2 - 1.2
# if `is_clipped` is true, all data below 0 is set to 0 and all data above 1 is set to 1
# expects a numpy array for `data`
def map_range(data, a1, a2, b1, b2, is_clipped):
    data = ( (data - a1) * (b2 - b1) / (a2 - a1) ) + b1
    if is_clipped:
        return np.clip(data, 0, 1)
    return data

def apply_filters(filters):
    global __image
    for filter in filters:
        __image = filter.run(__image, get_remapped_heatmap())

def get_output_image():
    return __image
