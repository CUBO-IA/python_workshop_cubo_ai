#!/usr/bin/env python3
"""Launcher for Duck Hunt.

If pygame is not importable from the current interpreter, re-exec this file
with the project's virtual environment interpreter (``.venv``), which has the
wheels installed. This keeps ``python3 run.py`` working even when the system
Python is too new for a pygame wheel.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(ROOT, ".venv", "bin", "python")


def _reexec_in_venv():
    """Restart this script with .venv/bin/python. Returns its exit code."""
    if not os.path.isfile(VENV_PYTHON):
        print(f"Error: pygame is not installed and no virtualenv was found at {VENV_PYTHON}.")
        print("Create one with:  uv venv --python 3.13 .venv && uv pip install -r requirements.txt")
        return 1

    env = dict(os.environ)
    # Avoid an infinite relaunch loop if the venv interpreter is the current one.
    env["DUCK_HUNT_NO_REEXEC"] = "1"
    return subprocess.call([VENV_PYTHON, os.path.abspath(__file__)], env=env)


def main():
    if not os.environ.get("DUCK_HUNT_NO_REEXEC"):
        try:
            import pygame  # noqa: F401
        except ModuleNotFoundError:
            return _reexec_in_venv()

    from src.app import Application

    app = Application()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
