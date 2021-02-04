class Attribute:
    def __init__(self, name, default_value, display):
        self.name = name
        self.display = display
        if (default_value != None):
            self.display.default = default_value
            self.value = default_value


class SliderAttribute:
    def __init__(self,  default = 0, min = None, max = None, step = 1, clampInput = False):
        self.value = default

        self.min = min
        self.max = max
        self.step = step
        self.clampInput = clampInput

class TextEntryAttribute:
    def __init__(self, default = 0, min = None, max = None, clampInput = False):
        self.value = default

        self.min = min
        self.max = max
        self.clampInput = clampInput

class RGBColorPickerAttribute:
    def __init__(self, default = (0,0,0)):
        self.value = default
