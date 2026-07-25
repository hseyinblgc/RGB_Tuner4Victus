# --------------------------
# HELPERS
# --------------------------
import colorsys
import subprocess


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
