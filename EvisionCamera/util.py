# -*- coding: utf-8 -*-
"""Utility module.
"""
import re
import platform
import cv2

from v4l import V4L2


class Utility():

    @staticmethod
    def support_format_list(device: int):
        system = Utility.get_os()
        if system == "linux" or system == "raspi":
            V4L2(device).support_format_list()
        else:
            WindowsUtil().support_format_list()

    @staticmethod
    def show_all(device: int):
        system = Utility.get_os()
        if system == "linux" or system == "raspi":
            V4L2(device).show_all()
        else:
            WindowsUtil().show_all()

    @staticmethod
    def show_param(device: int):
        system = Utility.get_os()
        if system == "linux" or system == "raspi":
            V4L2(device).show_param()
        else:
            WindowsUtil().support_format_list()

    @staticmethod
    def get_os() -> str:
        """Gets the type of current OS.

        Returns:
            str: A string which shows OS
        """
        system = platform.system()
        if re.search("linux", system, re.IGNORECASE):
            if re.search("armv", system, re.IGNORECASE):
                return "raspi"
            else:
                return "linux"
        elif re.search("windows", system, re.IGNORECASE):
            return "windows"
        else:
            return "Unknown"


class WindowsUtil():

    param_values = {
        "brightness": {
            "min": 0,
            "max": 255,
            "step": 1,
            "value": 128,
            "default": 128,
        },
        "contrast": {
            "min": 0,
            "max": 255,
            "step": 1,
            "value": 32,
            "default": 32,
        },
        "saturation": {
            "min": 0,
            "max": 255,
            "step": 1,
            "value": 32,
            "default": 32,
        },
        "gain": {
            "min": 0,
            "max": 255,
            "step": 1,
            "value": 64,
            "default": 64,
        },
        "sharpness": {
            "min": 0,
            "max": 255,
            "step": 1,
            "value": 24,
            "default": 24,
        },
    }

    cv_param_id = [
        cv2.CAP_PROP_BRIGHTNESS,
        cv2.CAP_PROP_CONTRAST,
        cv2.CAP_PROP_SATURATION,
        cv2.CAP_PROP_GAIN,
        cv2.CAP_PROP_SHARPNESS,
        #cv2.CAP_PROP_EXPOSURE,
        #cv2.CAP_PROP_AUTO_EXPOSURE
    ]

    fourcc_list = [
        "YUY2",
        "YUYV"]
    size_list = [
        "320x240",
        "640x480",
        "800x600",
        "1280x720",
        "1640x720",
        "1640x922",
        "1920x1080"]

    fps_list = [str(i) for i in range(5, 61, 5)]

    def __init__(self, parent=None):
        self.parent = parent

    def get_supported_params(self, device: int):
        lst = []
        for key in self.param_values.keys():
            lst.append(key)
        return lst

    def get_current_params(self, device: int, param_type: str = "full", plist: list = None):
        if param_type == "full":
            return self.param_values
        elif param_type == "selected":
            tmp = {}
            for param in plist:
                if param in self.param_values:
                    tmp[param] = self.param_values[param]
            return tmp

    def get_supported_fourcc(self, device: int):
        return self.fourcc_list

    def get_supported_size(self, device: int, fourcc: str):
        return self.size_list

    def get_supported_fps(self, device: int, fourcc: str, width: int, height: int):
        return self.fps_list

    def get_propID(self, param: str) -> int:
        if param == "brightness":
            return self.cv_param_id[0]
        elif param == "contrast":
            return self.cv_param_id[1]
        elif param == "saturation":
            return self.cv_param_id[2]
        elif param == "gain":
            return self.cv_param_id[3]
        elif param == "sharpness":
            return self.cv_param_id[4]
        elif param == "exposure_absolute":
            return self.cv_param_id[5]
        elif param == "exposure_auto":
            return self.cv_param_id[6]
        else:
            return None

    def support_format_list(self):
        pass

    def show_all(self):
        pass

    def show_param(self):
        pass
