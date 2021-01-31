class Attribute:
    def __init__(self, name, default_value, display):
        self.name = name
        self.display = display
        if (default_value != None):
            self.display.start = default_value
            self.value = default_value


class SliderDisplay:
    def __init__(self,  start = 0, min = None, max = None, step = 1, clampInput = False):
        self.value = start

        self.min = min
        self.max = max
        self.step = step
        self.clampInput = clampInput

class TextEntryDisplay:
    def __init__(self, start = 0, min = None, max = None, clampInput = False):
        self.value = start

        self.min = min
        self.max = max
        self.clampInput = clampInput

class ColorPickerDisplay:
    def __init__(self, start = [0,0,0]):
        self.value = start
