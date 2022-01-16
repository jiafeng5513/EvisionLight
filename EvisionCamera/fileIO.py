#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The utility class about file IO.
"""
from datetime import datetime
from pathlib import Path
from itertools import cycle


class FileIO():

    file_save_lst = [
        "Timestamp",
        "Manual",
        "Sequential",
    ]

    file_save = cycle(file_save_lst)

    @staticmethod
    def get_filename(pattern: str, ext: str, parent: Path = Path(".")) -> str:
        """Gets filename.

        Determines filename of image of video to save.
        Filename will be determined accroding to the format: <name field>.<ext>
        The name field has following three types.
            - Sequantial
                The filename will have a right-aligned, 5-digits serial number
                with zero-filled.
            - Timestamp
                The filename will have the time when the file is created.
            - Manual
                The filename will be determined by user.

        Args:
            pattern (str): The naming style of file.
            ext (str): The suffix.
            parent (Path, optional): A directory where the saved file is stored.
                Defaults to Path(".").

        Returns:
            str: Filename.
        """
        if pattern == "Sequential":
            index = 0
            index_str = "{:0>5}.{}".format(index, ext)
            filename = parent / index_str
            while index < 100000:
                if not filename.exists():
                    break
                index += 1
                index_str = "{:0>5}.{}".format(index, ext)
                filename = parent / index_str
        elif pattern == "Timestamp":
            now = datetime.strftime(datetime.now(), "%y%m%d-%H%M%S")
            image = "{}.{}".format(now, ext)
            filename = Path(parent) / image
        else:
            filename = None

        return str(filename)