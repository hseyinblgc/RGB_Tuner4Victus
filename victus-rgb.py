#!/usr/bin/env python3

import argparse
import colorsys
import math
import os
import subprocess
import sys
import time

parser = argparse.ArgumentParser(
    prog="victus-rgb",
    description="Control the keyboard RGB lighting on HP Victus laptops directly from Linux by writing RGB values to the Embedded Controller (EC).",
)
parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
parser.add_argument("--speed", type=int, default=5, help="Adjust speed.")

sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("current", help="Show current color.")
sub.add_parser("stop", help="Stop effects.")
sub.add_parser("rainbow", help="Cycle through all colors smoothly.")

set_preset = sub.add_parser("color", help="Preset colors.")
set_preset.add_argument(
    "value", nargs="+", help="Color preset or R G B value (255 0 0)."
)

p_breathe = sub.add_parser("breathe", help="Breathing effect.")
p_breathe.add_argument("color", nargs="+")

p_alt = sub.add_parser("alternate", help="Alternate between two colors.")
p_alt.add_argument("color", nargs="+")
# p_alt.add_argument("c2", nargs="+")

p_fade = sub.add_parser("fade", help="Fade between two colors.")
p_fade.add_argument("color", nargs="+")

args = parser.parse_args()

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8

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


# --------------------------
# SYSTEM
# --------------------------


def require_root():
    if os.geteuid() != 0:
        print("Run with sudo.")
        sys.exit(1)


def ensure_ec_access():

    if not os.path.exists("/sys/kernel/debug"):
        subprocess.run(
            ["mount", "-t", "debugfs", "none", "/sys/kernel/debug"], check=True
        )

    if not os.path.exists(EC_PATH):
        subprocess.run(["modprobe", "ec_sys", "write_support=1"], check=True)

    if not os.path.exists(EC_PATH):
        print("EC interface not available.")
        sys.exit(1)


# --------------------------
# EC ACCESS
# --------------------------


def write_rgb(r, g, b):

    data = bytes([r, g, b])

    with open(EC_PATH, "r+b", buffering=0) as f:
        f.seek(OFFSET)
        f.write(data)


def read_current():

    with open(EC_PATH, "rb") as f:
        f.seek(OFFSET)
        r, g, b = f.read(3)

    print(f"Current RGB: {r} {g} {b}")


# --------------------------
# HELPERS
# --------------------------


def speed_delay(speed):

    speed = max(1, min(speed, 10))

    return 0.12 - speed * 0.01


def hsv_to_rgb(h, s, v):

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))


def kill_previous():

    subprocess.run(
        ["pkill", "-f", "victus-rgb.*--worker"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


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
            usage()


def run_background():

    kill_previous()
    new_args = [sys.executable, sys.argv[0], "--worker"] + sys.argv[1:]

    subprocess.Popen(
        new_args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Effect started in background.")
    sys.exit(0)


# --------------------------
# EFFECTS
# --------------------------


def rainbow(speed=5):

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

    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

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


# --------------------------
# CLI
# --------------------------


def usage():

    print("Usage:")
    print("victus-rgb red")
    print("victus-rgb 255 0 0")
    print("victus-rgb current")
    print("victus-rgb rainbow")
    print("victus-rgb rainbow 8")
    print("victus-rgb breathe red")
    print("victus-rgb breathe red 7")
    print("victus-rgb alternate red blue")
    print("victus-rgb fade red blue")
    print("victus-rgb stop")

    sys.exit(1)


def main():

    require_root()
    ensure_ec_access()

    worker = args.worker

    match args.command:
        case "current":
            read_current()

        case "stop":
            kill_previous()
            print("Effects stopped.")

        case "rainbow":
            if not worker:
                run_background()
            rainbow(args.speed)

        case "breathe":
            c = parse_color(args.color)
            if not worker:
                run_background()
            breathe(c, args.speed)

        case "alternate":
            c1, c2 = parse_color(args.color)

            if not worker:
                run_background()
            alternate(c1, c2, args.speed)

        case "fade":
            c1, c2 = parse_color(args.color)

            if not worker:
                run_background()
            fade(c1, c2, args.speed)

        case "color":
            c = parse_color(args.value)
            kill_previous()
            write_rgb(*c)
        case _:
            usage()


if __name__ == "__main__":
    main()
