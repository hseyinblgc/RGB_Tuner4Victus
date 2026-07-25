#!/usr/bin/env python3

import argparse
import sys

from src.ea_access import (
    ensure_ec_access,
    read_current,
    require_root,
    run_background,
    write_rgb,
)
from src.effects import alternate, breathe, fade, rainbow
from src.helpers import kill_previous, list_colors, parse_color

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
            list_colors()

        case _:
            usage()


if __name__ == "__main__":
    try:
        main()
    except ValueError:
        usage()
