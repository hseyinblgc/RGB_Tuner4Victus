# --------------------------
# EFFECTS
# --------------------------
import math
import time

from src.ea_access import write_rgb
from src.helpers import hsv_to_rgb, rgb_to_hsv, speed_delay


def rainbow(speed: int = 5) -> None:

    delay = speed_delay(speed)
    hue = 0

    while True:
        write_rgb(*hsv_to_rgb(hue, 1, 1))

        hue += 0.003
        if hue >= 1:
            hue = 0

        time.sleep(delay)


def breathe(color, speed=5):

    delay = speed_delay(speed)
    MIN_BRIGHTNESS: int = 10

    h, s, _ = rgb_to_hsv(*color[0])

    steps = 100
    while True:
        for i in range(steps + 1):
            # Half-wave sine curve from 0 -> 1 -> 0
            phase = i / steps
            brightness = math.sin(phase * math.pi)
            # Scale between MIN_BRIGHTNESS and 1.0
            scaled = (MIN_BRIGHTNESS / 100) + brightness * (1 - MIN_BRIGHTNESS / 100)
            write_rgb(*hsv_to_rgb(h, s, scaled))
            time.sleep(delay)


def alternate(c1, c2, speed=5):

    delay = speed_delay(speed)

    while True:
        write_rgb(*c1)
        time.sleep(delay * 6)

        write_rgb(*c2)
        time.sleep(delay * 6)


def fade(c1, c2, speed=5):

    delay = speed_delay(speed)

    r1, g1, b1 = c1
    r2, g2, b2 = c2

    while True:
        for i in range(0, 101, 2):
            r = int(r1 + (r2 - r1) * (i / 100))
            g = int(g1 + (g2 - g1) * (i / 100))
            b = int(b1 + (b2 - b1) * (i / 100))

            write_rgb(r, g, b)
            time.sleep(delay)

        for i in range(100, -1, -2):
            r = int(r1 + (r2 - r1) * (i / 100))
            g = int(g1 + (g2 - g1) * (i / 100))
            b = int(b1 + (b2 - b1) * (i / 100))

            write_rgb(r, g, b)
            time.sleep(delay)
