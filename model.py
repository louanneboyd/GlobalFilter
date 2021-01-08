__image = None
__heatmap = None

def set_input_image(image):
    global __image
    __image = image

def set_input_heatmap(heatmap):
    global __heatmap
    __heatmap = heatmap

def apply_filters(filters):
    global __image
    for filter in filters:
        __image = filter.run(__image, __heatmap)

def get_output_image():
    return __image
