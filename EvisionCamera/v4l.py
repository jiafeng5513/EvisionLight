#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import subprocess
import re
import sys
from typing import Callable


class V4L2():

    def __init__(self, device: int = 0, width: int = 640, heigth: int = 480, fps: int = 30,
        fourcc: str = "YUYV", parent: object = None):
        self.device = device
        self.width = width
        self.height = heigth
        self.fps = fps
        self.fourcc = fourcc
        self.parent = parent

        self.fourcc_list = []
        self.vidcap_format = []
        #self.get_fourcc()
        #for cc in self.fourcc_list:
        #    self.get_fmt_size(cc)

    def show_fourcc(self):
        cmd = ["v4l2-ctl", "-d", str(self.device), "--list-formats"]
        self.run_v4l2cmd(cmd)

    def show_all(self):
        cmd = ["v4l2-ctl", "-d", str(self.device), "--list-formats-ext"]
        self.run_v4l2cmd(cmd)

    def show_param(self):
        cmd = ["v4l2-ctl", "-d", str(self.device), "-L"]
        self.run_v4l2cmd(cmd)

    def run_v4l2cmd(self, cmd: str, stdout: bool = True):
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(self.device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        output = ret.stdout.decode()
        if stdout:
            print(output)
        else:
            return output

    @staticmethod
    def get_supported_fourcc(device: int) -> list:
        cmd = ["v4l2-ctl", "-d", str(device), "--list-formats"]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        fmt = ret.stdout.decode()

        lst = []
        pixel_format = r"\s+'"
        match = re.finditer(pixel_format, fmt)
        for index, m in enumerate(match):
            start = m.end()
            end = m.end()
            while end != len(fmt):
                end += 1
                if fmt[end] == "'":
                    break
            fourcc = fmt[start:end]
            if fourcc not in lst:
                lst.append(fmt[start:end])
        return lst

    @staticmethod
    def get_supported_size(device: int, fourcc: str) -> list:
        cmd = ["v4l2-ctl", "-d", str(device), "--list-framesize={}".format(fourcc)]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        ret = ret.stdout.decode()

        pattern = r"[0-9]+x[0-9]+"
        match = re.findall(pattern, ret)
        return match
    """
        lst = []
        for m in match:
            width, height = map(int, m.split("x"))
            self.get_fps(name, width, height)
"""

    @staticmethod
    def get_supported_fps(device: int, fourcc: str, width: int, height: int) -> list:
        cmd = [
            "v4l2-ctl",
            "-d",
            str(device),
            "--list-frameintervals=width={},height={},pixelformat={}".format(width, height, fourcc)
        ]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        ret = ret.stdout.decode()

        fps = "[0-9]+.[0-9]+ fps"
        lst = re.findall(fps, ret)
        return ["{}".format(item[:-3]) for item in lst]

    def support_format_list(self):
        self.get_fourcc()
        print("{:^10} | {:^10} | {:^10} | {:^10}".format("Fourcc", "Width", "Height", "FPS"))
        print("-" * 60)
        for i in self.vidcap_format:
            #print("-" * 60)
            print("{:^10} | {:^10} | {:^10} | {:^10}".format(*i))

        """
        with open("test.csv", "w") as f:
            for form in self.vidcap_format:
                data = ",".join(str(i) for i in form)
                f.write(data)
                f.write("\n")
        """

    def get_fourcc(self):
        cmd = ["v4l2-ctl", "-d", str(self.device), "--list-formats"]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(self.device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        fmt = ret.stdout.decode()
        pixel_format = r"\s+'"
        match = re.finditer(pixel_format, fmt)
        for index, m in enumerate(match):
            start = m.end()
            end = m.end()
            while end != len(fmt):
                end += 1
                if fmt[end] == "'":
                    break
            fourcc = fmt[start:end]
            if fourcc not in self.fourcc_list:
                self.fourcc_list.append(fmt[start:end])
        for cc in self.fourcc_list:
            self.get_fmt_size(cc)

    def get_fmt_size(self, name: str):
        cmd = ["v4l2-ctl", "-d", str(self.device), "--list-framesize={}".format(name)]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(self.device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        ret = ret.stdout.decode()

        pattern = r"[0-9]+x[0-9]+"
        match = re.findall(pattern, ret)
        for m in match:
            width, height = map(int, m.split("x"))
            self.get_fps(name, width, height)

    def get_fps(self, name: str, width: int, height: int):
        cmd = [
            "v4l2-ctl",
            "-d",
            str(self.device),
            "--list-frameintervals=width={},height={},pixelformat={}".format(width, height, name)
        ]
        ret = subprocess.run(cmd, stdout=subprocess.PIPE)
        if ret.returncode:
            print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(self.device),
                file=sys.stderr)
            sys.exit(ret.returncode)
        ret = ret.stdout.decode()

        fps = "[0-9]+.[0-9]+ fps"
        fps = re.findall(fps, ret)
        for f in fps:
            fmt = (name, width, height, float(f[:-3].strip()))
            self.vidcap_format.append(fmt)
        #print(self.vidcap_format)

    def set_vidcap_format(self):
        cmd = [
            "v4l2-ctl",
            "-d",
            str(self.device),
            "--set-fmt-video=width={},height={},pixelformat={}".format(self.width, self.height, self.fourcc)
        ]
        cmd2 = [
            "v4l2-ctl",
            "-d",
            str(self.device),
            "-p",
            "{:.0f}".format(self.fps)
        ]
        for c in [cmd, cmd2]:
            ret = subprocess.run(c, stdout=subprocess.PIPE)
            if ret.returncode:
                print("An error occured while executing v4l2 command. \nCheck if /dev/video{} exists, then reconnect the camera to PC.".format(self.device),
                    file=sys.stderr)
                sys.exit(ret.returncode)

    def get_vidcap_format(self, data: str) -> list:
        buf = []
        if data == "fourcc":
            for item in self.vidcap_format:
                target = item[0]
                if target not in buf:
                    buf.append(target)
        elif data == "size":
            for item in self.vidcap_format:
                width = item[1]
                height = item[2]
                target = "{}x{}".format(width, height)
                if target not in buf:
                    buf.append(target)
        elif data == "fps":
            for item in self.vidcap_format:
                target = str(item[3])
                if target not in buf:
                    buf.append(str(target))
        else:
            return None
        return buf

    def get_params(self, ptype: str = "full", *plist) -> dict:
        cmd = ["v4l2-ctl", "-d", str(self.device), "-l"]
        ret = subprocess.check_output(cmd)
        v4l2_output = ret.decode()
        v4l2_output = self.extract_vidcap_params(v4l2_output).strip().split("\n")
        dict_ = {}
        if ptype == "full":
            for param in v4l2_output:
                sub_dict = {}
                tmp = param.split()
                if len(tmp) > 3:
                    pass
                    name = tmp[0]
                    hex_ = tmp[1]
                    type_ = tmp[2]
                    values = self.retreive(param)
                    sub_dict["hex"] = hex_
                    sub_dict["type"] = type_
                    sub_dict.update(values)
                    dict_.update({name: sub_dict})
            return dict_
        else:
            for p in plist:
                for param in v4l2_output:
                    if re.search(p, param):
                        sub_dict = {}
                        tmp = param.split()
                        name = tmp[0]
                        hex_ = tmp[1]
                        type_ = tmp[2]
                        values = self.retreive(param)
                        sub_dict["hex"] = hex_
                        sub_dict["type"] = type_
                        sub_dict.update(values)
                        dict_.update({name: sub_dict})
                        self.params = dict_
            return dict_

    @staticmethod
    def retreive(target: str) -> dict:
        value_list = {
            "min": 0,
            "max": 0,
            "step": 0,
            "value": 0,
            "default": 0,
            "flags": "init"
        }
        for key, value in value_list.items():
            m = re.search(key, target)
            if m:
                start = m.start()
                end = start
                while end != len(target):
                    if target[end] == " ":
                        break
                    end += 1
                tmp = target[start:end]
                tmp = tmp.split("=")
                try:
                    value_list[key] = int(tmp[1])
                except:
                    value_list[key] = str(tmp[1])
            else:
                value_list[key] = None
        return value_list

    def get_param_value(self, param: str, propID: int) -> dict:
        """Get properties of specified parameter.

        Get the max, min, cuurent calue, change step of the spcefied parameter. These value
        can be obtained by v4l2-ctl library.

        Args:
            param (str): Added parameter
            propID (int): Property ID of added parameter. This is defined in opencv module.

        Returns:
            dict: [description]
        """
        # Make list of property. Each value set inital value ( = 0).
        value_list = {
            "max": 0,
            "min": 0,
            "step": 0,
            "value": 0,
            "propID": propID
        }

        cmd = ["v4l2-ctl", "-d", str(self.device), "-l"]
        ret = subprocess.check_output(cmd)
        v4l2_output = ret.decode().strip().split("\n")

        index = 0
        for v in v4l2_output:
            if param in v:
                break
            index += 1

        p_str = v4l2_output[index]
        for key in value_list.keys():
            m = re.search(key, p_str)
            if m:
                end = m.start()
                while end != len(p_str):
                    if not p_str[end] == " ":
                        end += 1
                    else:
                        break
                target = p_str[m.start():end]
                v = target.split("=")
                value_list[key] = int(v[1])
        return value_list

    @staticmethod
    def change_param(device: int, param: str, value: int, func: Callable) -> bool:
        """Change a paramter value.

        This method will be called when user change a parameter by its slider.

        Args:
            value (int): Value to be set.
        """
        cmd = ["v4l2-ctl", "-d", str(device), "--set-ctrl", "{}={}".format(param, value)]
        ret = subprocess.call(cmd)
        if ret:
            func("Input parameter ({}) is invalid !".format(param), color="red")
            return False
        else:
            return True


    @staticmethod
    def set_param_default(device: int, current_param: dict, func: Callable):
        for param, val in current_param.items():
            default = val["default"]
            cmd = ["v4l2-ctl", "-d", str(device), "--set-ctrl", "{}={}".format(param, default)]
            ret = subprocess.call(cmd)
            if ret:
                func("Input parameter is invalid !", color="red")
                return -1
            current_param[param]["slider_val"] = default
        return current_param

    @staticmethod
    def get_supported_params(device: str) -> list:
        cmd = ["v4l2-ctl", "-d", str(device), "-l"]
        ret = subprocess.check_output(cmd)
        v4l2_output = ret.decode()
        v4l2_output = V4L2.extract_vidcap_params(v4l2_output).strip().split("\n")
        lst = []
        for param in v4l2_output:
            tmp = param.split()
            if len(tmp) > 3:
                lst.append(tmp[0])
        return lst

    @staticmethod
    def extract_vidcap_params(string: str, pattern: str = "videocapture") -> str:
        user = "User Controls"
        codec = "Codec Controls"
        camera = "Camera Controls"
        jpeg = "JPEG Compression Controls"

        # index
        start, end = 0, 0

        if pattern == "videocapture":
            m1 = re.search(user, string)
            if m1:
                start = m1.end()
            m2 = re.search(codec, string)
            if m2:
                end = m2.start()
            else:
                end = -1
            s = string[start:end]
            m3 = re.search(camera, string)
            if m3:
                start = m3.end()
            else:
                return s
            m4 = re.search(jpeg, string)
            if m4:
                end = m4.start()
            else:
                return s
            s += string[start:end]
            return s

    @staticmethod
    def get_current_params(device: int, param_type: str, plist: list = None) -> dict:
        cmd = ["v4l2-ctl", "-d", str(device), "-l"]
        ret = subprocess.check_output(cmd)
        v4l2_output = ret.decode()
        v4l2_output = V4L2.extract_vidcap_params(v4l2_output).strip().split("\n")
        dict_ = {}
        if param_type == "full":
            for param in v4l2_output:
                sub_dict = {}
                tmp = param.split()
                if len(tmp) > 3:
                    pass
                    name = tmp[0]
                    hex_ = tmp[1]
                    type_ = tmp[2]
                    values = V4L2.retreive(param)
                    sub_dict["hex"] = hex_
                    sub_dict["type"] = type_
                    sub_dict.update(values)
                    dict_.update({name: sub_dict})
            return dict_
        else:
            for p in plist:
                for param in v4l2_output:
                    if re.search(p, param):
                        sub_dict = {}
                        tmp = param.split()
                        name = tmp[0]
                        hex_ = tmp[1]
                        type_ = tmp[2]
                        values = V4L2.retreive(param)
                        sub_dict["hex"] = hex_
                        sub_dict["type"] = type_
                        sub_dict.update(values)
                        dict_.update({name: sub_dict})
                        #self.params = dict_
            return dict_



if __name__ == '__main__':

    desc = '''
description'''

    epi = '''
--------------------------- example ---------------------------------

- epi
>>> python %(prog)s args
---------------------------------------------------------------------'''

    parser = argparse.ArgumentParser(
        description=desc,
        epilog=epi,
)
    args = parser.parse_args()

    print(V4L2.get_supported_params(0))
    from pprint import pprint
    pprint(V4L2.get_current_params(0, "full"))