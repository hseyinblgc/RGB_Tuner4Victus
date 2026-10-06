# --------------------------
# HELPERS
# --------------------------
import colorsys
import sys
from itertools import batched


def speed_delay(speed: int) -> float:

    speed = max(1, min(speed, 10))

    return 0.12 - speed * 0.01


def hsv_to_rgb(h, s, v):

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))


def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s, v


PRESET_COLORS = {
    "blood_orange": (180, 40, 0),
    "blue": (0, 0, 255),
    "charcoal": (54, 69, 79),
    "cyan": (0, 255, 255),
    "cyber_violet": (74, 20, 140),
    "dark_amber": (153, 101, 21),
    "dark_slate": (47, 79, 79),
    "deep_emerald": (9, 77, 44),
    "eggplant": (75, 0, 130),
    "forest_green": (34, 139, 34),
    "green": (0, 255, 0),
    "maroon": (128, 0, 0),
    "midnight_blue": (25, 25, 112),
    "neon_purple": (100, 12, 223),
    "purple": (255, 0, 255),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
}


def list_colors() -> None:
    print("Available preset colors:")
    for color_name in PRESET_COLORS:
        print(f"  - {color_name}")
    sys.exit(0)


RGB = tuple[int, int, int]


def parse_color(*args: str) -> list[RGB]:
    rgb: list[RGB]

    if len(args) not in (1, 2, 3, 6):
        raise ValueError("Invalid argument")

    try:
        if len(args) in (1, 2):
            rgb = [PRESET_COLORS[arg.lower()] for arg in args]
        else:
            rgb = [(r, g, b) for r, g, b in batched(map(int, args), 3)]
    except KeyError as e:
        raise ValueError(f"Unknown color: {e.args[0]}") from None
    except ValueError:
        raise ValueError("RGB values must be integers") from None

    return rgb
