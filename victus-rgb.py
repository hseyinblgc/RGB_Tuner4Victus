#!/usr/bin/env python3

import argparse
import subprocess
import sys

from src.ea_access import ensure_ec_access, read_current, require_root, write_rgb
from src.effects import alternate, breathe, fade, rainbow
from src.helpers import kill_previous

parser = argparse.ArgumentParser(
    prog="victus-rgb",
    description="Control the keyboard RGB lighting on HP Victus laptops directly from Linux by writing RGB values to the Embedded Controller (EC).",
)
parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
parser.add_argument("--speed", type=int, default=5, help="Adjust speed.")

sub = parser.add_subparsers(dest="command", required=True)
sub.add_parser("list", help="List available color presets.")
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
# CLI
# --------------------------


def usage() -> None:
    parser.print_help()
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
            write_rgb(*c[0])

        case "list":
            print("Available preset colors:")
            for color_name in PRESET_COLORS:
                print(f"  - {color_name}")
            sys.exit(0)

        case _:
            usage()


if __name__ == "__main__":
    main()
