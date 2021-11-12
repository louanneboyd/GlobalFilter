from filters.accurate_blur import AccurateBlur
from filters.fade_to_color import FadeToColor
from filters.desaturate import Desaturate
from filters.fast_blur import FastBlur
from filters.luminance import Luminance
from filters.luminance_absolute import LuminanceAbsolute

available_filters = [
    AccurateBlur,
    Desaturate,
    FadeToColor,
    FastBlur,
    Luminance,
    LuminanceAbsolute
]

# sort the filters alphabetically
available_filters.sort(key=lambda filter: filter.name, reverse=True)
