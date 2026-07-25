# --------------------------
# HELPERS
# --------------------------
import colorsys
import subprocess
import sys


def speed_delay(speed: int) -> float:

    speed = max(1, min(speed, 10))

    return 0.12 - speed * 0.01


def hsv_to_rgb(h, s, v):

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))


def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s, v


def kill_previous():

    subprocess.run(
        ["pkill", "-f", "victus-rgb.*--worker"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


PRESET_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "purple": (255, 0, 255),
    "neon-purple": (100, 12, 223),
    "white": (255, 255, 255),
    "fire": (255, 60, 0),
    "flame": (255, 90, 0),
    "off": (0, 0, 0),
}


def list_colors() -> None:
    print("Available preset colors:")
    for color_name in PRESET_COLORS:
        print(f"  - {color_name}")
    sys.exit(0)


def parse_color(values: list[str]) -> list[tuple]:
    match values:
        case [color] if color.lower() in PRESET_COLORS:
            return [PRESET_COLORS[color.lower()]]

        case [color1, color2] if (
            color1.lower() in PRESET_COLORS and color2.lower() in PRESET_COLORS
        ):
            return [PRESET_COLORS[color1.lower()], PRESET_COLORS[color2.lower()]]

        case [r, g, b]:
            try:
                return [(int(r), int(g), int(b))]
            except ValueError:
                print("RGB values must be integers")
                sys.exit(1)

        case [r1, g1, b1, r2, g2, b2]:
            try:
                return [(int(r1), int(g1), int(b1)), (int(r2), int(g2), int(b2))]
            except ValueError:
                print("RGB values must be integers")
                sys.exit(1)

        case _:
            raise ValueError("Invalid argument")
            sys.exit(1)
