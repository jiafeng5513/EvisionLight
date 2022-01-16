#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path


def to_abspath(path):
    dir_ = "icon/"
    path = dir_ + path
    return Path(path).resolve().as_posix()


class Icon():

    class Light():
        save = to_abspath("light/no_transparency_help.png")
        stop = to_abspath("light/no_transparency_stop.png")
        start = to_abspath("light/no_transparency_start.png")
        close = to_abspath("light/no_transparency_close.png")
        usage = to_abspath("light/no_transparency_help.png")
        toggle_off = to_abspath("light/no_transparency_toggle_off.png")
        toggle_on = to_abspath("light/no_transparency_toggle_on.png")


    class Dark():
        save = to_abspath("no_transparency_help.png")
        stop = to_abspath("no_transparency_stop.png")
        start = to_abspath("no_transparency_start.png")
        #close = to_abspath("dark/close.png")
        close = to_abspath("dark/no_transparency_close.png")
        usage = to_abspath("dark/no_transparency_help.png")
        toggle_off = to_abspath("no_transparency_toggle_off.png")
        toggle_on = to_abspath("no_transparency_toggle_on.png")



if __name__ == "__main__":
    print(Icon.Light.save)
