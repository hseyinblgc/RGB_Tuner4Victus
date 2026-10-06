#!/usr/bin/env python3

import argparse
import sys
from enum import Enum

from src.core import kill_previous, read_current, run_background, write_rgb
from src.effects import alternate, breathe, fade, rainbow
from src.helpers import list_colors, parse_color


class Command(str, Enum):
    LIST = "list"
    CURRENT = "current"
    STOP = "stop"
    RAINBOW = "rainbow"
    COLOR = "color"
    BREATHE = "breathe"
    ALTERNATE = "alternate"
    FADE = "fade"


def launch(args, effect, *effect_args):
    if not args.worker:
        run_background()
    effect(*effect_args, args.speed)


def stop(_):
    kill_previous()
    print("Effects stopped.")


def set_color(a):
    c = parse_color(*a.color)
    kill_previous()
    write_rgb(*c[0])


# command -> (help text, nargs, handler)
COMMANDS = {
    Command.LIST: ("List available color presets.", None, lambda a: list_colors()),
    Command.CURRENT: ("Show current color.", None, lambda a: read_current()),
    Command.STOP: ("Stop effects.", None, stop),
    Command.RAINBOW: (
        "Cycle through all colors smoothly.",
        None,
        lambda a: launch(a, rainbow),
    ),
    Command.COLOR: ("Preset colors.", "+", set_color),
    Command.BREATHE: (
        "Breathing effect.",
        "+",
        lambda a: launch(a, breathe, parse_color(*a.color)),
    ),
    Command.ALTERNATE: (
        "Alternate between two colors.",
        "+",
        lambda a: launch(a, alternate, *parse_color(*a.color)),
    ),
    Command.FADE: (
        "Fade between two colors.",
        "+",
        lambda a: launch(a, fade, *parse_color(*a.color)),
    ),
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="victus-rgb",
        description="Control the keyboard RGB lighting on HP Victus laptops directly from Linux by writing RGB values to the Embedded Controller (EC).",
    )
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--speed", type=int, default=5, help="Adjust speed.")

    sub = parser.add_subparsers(dest="command", required=True)

    for cmd, (help_text, nargs, handler) in COMMANDS.items():
        p = sub.add_parser(cmd.value, help=help_text)
        if nargs is not None:
            p.add_argument(
                "color", nargs=nargs, help="Color preset or R G B value (255 0 0)."
            )
        p.set_defaults(func=handler)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ValueError:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
