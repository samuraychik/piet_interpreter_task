from enum import IntEnum


class Light(IntEnum):
    LIGHT = 0
    NORMAL = 1
    DARK = 2


class Hue(IntEnum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    CYAN = 3
    BLUE = 4
    MAGENTA = 5


HEX_COLORS = {
    "#ffc0c0": {"light": Light.LIGHT, "hue": Hue.RED},
    "#ffffc0": {"light": Light.LIGHT, "hue": Hue.YELLOW},
    "#c0ffc0": {"light": Light.LIGHT, "hue": Hue.GREEN},
    "#c0ffff": {"light": Light.LIGHT, "hue": Hue.CYAN},
    "#c0c0ff": {"light": Light.LIGHT, "hue": Hue.BLUE},
    "#ffc0ff": {"light": Light.LIGHT, "hue": Hue.MAGENTA},
    "#ff0000": {"light": Light.NORMAL, "hue": Hue.RED},
    "#ffff00": {"light": Light.NORMAL, "hue": Hue.YELLOW},
    "#00ff00": {"light": Light.NORMAL, "hue": Hue.GREEN},
    "#00ffff": {"light": Light.NORMAL, "hue": Hue.CYAN},
    "#0000ff": {"light": Light.NORMAL, "hue": Hue.BLUE},
    "#ff00ff": {"light": Light.NORMAL, "hue": Hue.MAGENTA},
    "#c00000": {"light": Light.DARK, "hue": Hue.RED},
    "#c0c000": {"light": Light.DARK, "hue": Hue.YELLOW},
    "#00c000": {"light": Light.DARK, "hue": Hue.GREEN},
    "#00c0c0": {"light": Light.DARK, "hue": Hue.CYAN},
    "#0000c0": {"light": Light.DARK, "hue": Hue.BLUE},
    "#c000c0": {"light": Light.DARK, "hue": Hue.MAGENTA},
    }

HEX_WHITE = "#ffffff"
HEX_BLACK = "#000000"
