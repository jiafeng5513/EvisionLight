#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import sys
from abc import ABCMeta, abstractmethod
import cv2
from EvisionCamera.v4l import V4L2
from EvisionCamera.util import WindowsUtil


#class Camera(metaclass=ABCMeta):
class Camera():
    """The Base class for handling USB camera
    """

    def __init__(self, device: int, colorspace="rgb", parent=None):
        self.device = device
        self.colorspace = colorspace
        self.parent = parent
        self.is_reading = True
        self.is_recording = False

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def get_supported_params(self):
        pass

    @abstractmethod
    def get_current_params(self):
        pass

    @abstractmethod
    def get_supported_fourcc(self):
        pass

    @abstractmethod
    def get_supported_size(self):
        pass

    @abstractmethod
    def get_supported_fps(self):
        pass

    @abstractmethod
    def set_parameter(self):
        pass

    @abstractmethod
    def set_param_default(self):
        pass

    def open(self):
        """Creates an opencv VideoCapture object.
        """
        self.capture = cv2.VideoCapture(self.device)
        if not self.capture.isOpened():
            self.open_error()
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def open_error(self):
        """Shows error meesage, finishes the all program.

        This method will be called when the PC cannot detect an USB camera,
        """
        print("cannot open /dev/video{0}. Check if /dev/video{0} exists, then reconnect the camera".format(self.device), file=sys.stderr)
        sys.exit(-1)

    def init(self):
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        if self.fps:
            self.sec = 1 / self.fps
        else:
            self.sec = 1 / 30.0

    def start_frame(self):
        """Start Reading frame
        """
        self.is_reading = True
        self.parent.write_text("Start Reading frame")

    def stop_frame(self):
        """Stop Reading frame
        """
        self.is_reading = False
        self.parent.write_text("Stop Reading frame")

    def start_recording(self, filename: str, codec: str):
        """Creates an opencv VideoWriter object to start recording.
        """
        self.create_videowriter(filename, codec)
        self.is_recording = True
        self.parent.write_text("Start Recording")

    def stop_recording(self):
        """Finishes recording to save the video file.
        """
        self.is_recording = False
        self.video_writer.release()
        self.parent.write_text("Finish Recording")

    def create_videowriter(self, filename: str, codec: str):
        """Creates an opencv VideoWriter object

        Args:
            filename (str): Filename of video
            codec (str): Codec
        """
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.video_writer = cv2.VideoWriter(
            filename,
            fourcc,
            self.capture.get(cv2.CAP_PROP_FPS),
            (
                int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                )
            )

    def read_frame(self):
        """Reads one frame from the connected camera.

        If a flag for the frame set true, One frame is read from the camera as
        the type of numpy.ndarray. To rearrange the channel's order, convert the
        frame from BRG to RGB if the colorspace is set to color (by default).
        If grayscale, the frame will be convertd to 1 channel grayscale.
        """
        if self.is_reading:
            ret, cv_image = self.capture.read()
            if not ret:
                self.parent.write_text("cannot read the next frame.")
                sys.exit(-1)
            if self.is_recording:
                self.video_writer.write(cv_image)
            else:
                # Convert the order of channel from BGR to RGB
                if self.colorspace == "rgb":
                    self.frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                elif self.colorspace == "gray":
                    self.frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                else:
                    self.frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    def get_properties(self) -> list:
        """Gets the current width, height, fps and fourcc of camera.

        Returns:
            list: width, height, fps and fourcc of camera
        """
        lst = []
        lst.append(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        lst.append(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        lst.append(self.decode_fourcc(self.capture.get(cv2.CAP_PROP_FOURCC)))
        lst.append(self.capture.get(cv2.CAP_PROP_FPS))
        return lst

    def set_properties(self, fourcc: str, width: int, height: int, fps: float):
        """Sets the current width, height, fps and fourcc of camera.

        Args:
            fourcc (str): Fourcc
            width (int): Frame width
            height (int): Frame heigth
            fps (float): Frame FPS
        """
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)
        self.size = "{}x{}".format(width, height)

        self.parent.write_text("Change frame properties")
        self.parent.write_text("-" * 80)
        self.parent.write_text("{:<10} : {}".format("fourcc", self.decode_fourcc(self.capture.get(cv2.CAP_PROP_FOURCC))))
        self.parent.write_text("{:<10} : {}".format("width", width))
        self.parent.write_text("{:<10} : {}".format("height", height))
        self.parent.write_text("{:<10} : {}".format("FPS", fps))
        self.parent.write_text("-" * 80)

    def decode_fourcc(self, v: float) -> str:
        """Decode the return value.

        Args:
            v (float): [description]

        Returns:
            str: Fourcc such as YUYV, MJPG, etc.

        Examples:
            >>> decoder_fourcc(1448695129.0)
            >>> "YUYV"
        """
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])


class LinuxCamera(Camera):

    font_family = "Note Sans"
    font_size = 14

    def __init__(self, device: int, color: str = "rgb", parent=None):
        super().__init__(device, color, parent)
        super().open()

    def get_supported_params(self) -> list:
        return V4L2.get_supported_params(self.device)

    def get_current_params(self, param_type: str, *plist: list) -> dict:
        return V4L2.get_current_params(self.device, param_type, *plist)

    def get_supported_fourcc(self) -> list:
        return V4L2.get_supported_fourcc(self.device)

    def get_supported_size(self, fourcc: str) -> list:
        return V4L2.get_supported_size(self.device, fourcc)

    def get_supported_fps(self, fourcc: str, width: int, height: int) -> list:
        return V4L2.get_supported_fps(self.device, fourcc, width, height)

    def set_parameter(self, param: str, value: int):
        try:
            self.is_reading = False
            V4L2.change_param(self.device, param, value, self.parent.write_text)
        finally:
            self.is_reading = True


class WindowsCamera(Camera):

    font_family = "Yu Gothic"
    font_size = 20

    def __init__(self, device: int, color: str = "rgb", parent=None):
        super().__init__(device, color, parent)
        self.windows = WindowsUtil()
        self.open()

    def open(self):
        self.capture = cv2.VideoCapture(self.device, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.open_error()
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.color = "rgb"

    def get_supported_params(self) -> list:
        return self.windows.get_supported_params(self.device)

    def get_current_params(self, param_type: str, plist: list = None) -> dict:
        return self.windows.get_current_params(self.device, param_type, plist)

    def get_supported_fourcc(self) -> list:
        return self.windows.get_supported_fourcc(self.device)

    def get_supported_size(self, fourcc: str) -> list:
        return self.windows.get_supported_size(self.device, fourcc)

    def get_supported_fps(self, fourcc: str, width: int, height: int) -> list:
        return self.windows.get_supported_fps(self.device, fourcc, width, height)

    def set_parameter(self, param: str, value: int) -> int:
        try:
            self.is_reading = False
            propID = self.windows.get_propID(param)
            ret = self.capture.set(propID, value)
            if not ret:
                self.parent.write_text("Input parameter is invalid !", level="err", color="red")
            self.is_reading = True
            return value
        finally:
            self.is_reading = True


class RaspiCamera(Camera):

    def __init__(self, device: int, color: str = "rgb", parent=None):
        super().__init__(device, color, parent)
        super().open()

    def get_supported_params(self) -> list:
        return V4L2.get_supported_params(self.device)

    def get_current_params(self, param_type: str, plist: list) -> dict:
        return V4L2.get_current_params(self.device, param_type, plist)

    def get_supported_fourcc(self) -> list:
        return V4L2.get_supported_fourcc(self.device)

    def get_supported_size(self, fourcc: str) -> list:
        return V4L2.get_supported_size(self.device, fourcc)

    def get_supported_fps(self, fourcc: str, width: int, height: int) -> list:
        return V4L2.get_supported_fps(self.device, fourcc, width, height)

    def set_parameter(self, param: str, value: int):
        try:
            self.is_reading = False
            V4L2.change_param(self.device, param, value, self.parent.write_text)
        finally:
            self.is_reading = True
