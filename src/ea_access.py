# --------------------------
# EC ACCESS
# --------------------------
import os
import subprocess
import sys

from src.helpers import kill_previous

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
OFFSET = 8


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


def run_background():
    kill_previous()

    if getattr(sys, "frozen", False):
        new_args = [sys.executable, "--worker"] + sys.argv[1:]

    else:
        new_args = [sys.executable, sys.argv[0], "--worker"] + sys.argv[1:]

    subprocess.Popen(
        new_args,
        env={**os.environ, "PYINSTALLER_RESET_ENVIRONMENT": "1"}, # I googled for that xd
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print("Effect started in background.")
    sys.exit(0)
