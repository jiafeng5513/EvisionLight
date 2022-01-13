import os
import sys
from ctypes import *

current_platform = sys.platform
if current_platform == 'win32':
    EvisionLogLibrary = cdll.LoadLibrary('../../../install/EvisionLog.dll')
    encoding = 'gbk'
else:
    EvisionLogLibrary = cdll.LoadLibrary('../../../install/EvisionLog.so')
    encoding = 'utf8'

_EvisionLogInit = EvisionLogLibrary.EvisionLogInit
_EvisionConsoleLogInfo = EvisionLogLibrary.EvisionConsoleLogInfo
_EvisionConsoleLogDebug = EvisionLogLibrary.EvisionConsoleLogDebug
_EvisionConsoleLogWarning = EvisionLogLibrary.EvisionConsoleLogWarning
_EvisionConsoleLogError = EvisionLogLibrary.EvisionConsoleLogError
_EvisionFileLogInfo = EvisionLogLibrary.EvisionFileLogInfo
_EvisionFileLogDebug = EvisionLogLibrary.EvisionFileLogDebug
_EvisionFileLogWarning = EvisionLogLibrary.EvisionFileLogWarning
_EvisionFileLogError = EvisionLogLibrary.EvisionFileLogError

_EvisionConsoleLogInfo.argtypes = [POINTER(c_char), c_int]
_EvisionConsoleLogDebug.argtypes = [POINTER(c_char), c_int]
_EvisionConsoleLogWarning.argtypes = [POINTER(c_char), c_int]
_EvisionConsoleLogError.argtypes = [POINTER(c_char), c_int]
_EvisionFileLogInfo.argtypes = [POINTER(c_char), c_int]
_EvisionFileLogDebug.argtypes = [POINTER(c_char), c_int]
_EvisionFileLogWarning.argtypes = [POINTER(c_char), c_int]
_EvisionFileLogError.argtypes = [POINTER(c_char), c_int]


class EvisionLog(object):
    def __init__(self):
        pass

    @staticmethod
    def convert_str(msg):
        msg_bytes = bytes(msg, encoding)
        bytes_length = len(msg_bytes)
        msg_str = (c_char*bytes_length)(*msg_bytes)
        cast(msg_str, POINTER(c_char))
        return msg_str, bytes_length

    @staticmethod
    def init_logger():
        _EvisionLogInit()
        pass

    class Console(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionConsoleLogDebug(msg_str, bytes_length)
            pass

        @staticmethod
        def info(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionConsoleLogInfo(msg_str, bytes_length)
            pass

        @staticmethod
        def warning(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionConsoleLogWarning(msg_str, bytes_length)
            pass

        @staticmethod
        def error(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionConsoleLogError(msg_str, bytes_length)
            pass

    class File(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogDebug(msg_str, bytes_length)
            pass

        @staticmethod
        def info(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogInfo(msg_str, bytes_length)
            pass

        @staticmethod
        def warning(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogWarning(msg_str, bytes_length)
            pass

        @staticmethod
        def error(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogError(msg_str, bytes_length)
            pass

if __name__ == '__main__':
    EvisionLog.init_logger()
    EvisionLog.Console.debug("调试调试")
    EvisionLog.Console.info("信息信息")
    EvisionLog.Console.warning("调试信息")
    EvisionLog.Console.error("调试信息")

    EvisionLog.File.debug("调试调试")
    EvisionLog.File.info("信息信息")
    EvisionLog.File.warning("调试信息")
    EvisionLog.File.error("调试信息")