import os
import sys
from ctypes import *

current_platform = sys.platform
evision_log_path = os.path.dirname(os.path.abspath(__file__))
install_path = os.path.join(evision_log_path, "../install")
if current_platform == 'win32':
    if os.path.exists(os.path.join(install_path, 'EvisionLog.dll')):
        EvisionLogLibrary = cdll.LoadLibrary(os.path.join(install_path, 'EvisionLog.dll'))
    elif os.path.exists(os.path.join(install_path, 'libEvisionLog.dll')):
        EvisionLogLibrary = CDLL(os.path.join(install_path, 'libEvisionLog.dll'), winmode=101)
    else:
        raise RuntimeError("can not find dynamic link library for EvisionLog!")
    encoding = 'gbk'
else:
    EvisionLogLibrary = cdll.LoadLibrary(os.path.join(install_path, 'EvisionLog.so'))
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

_EvisionLogInit.argtypes = [POINTER(c_char), c_int]
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
    def init_logger(log_path):
        log_path_str, bytes_length = EvisionLog.convert_str(log_path)
        _EvisionLogInit(log_path_str, bytes_length)
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

    class All(object):
        def __init__(self):
            pass

        @staticmethod
        def debug(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogDebug(msg_str, bytes_length)
            _EvisionConsoleLogDebug(msg_str, bytes_length)
            pass

        @staticmethod
        def info(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogInfo(msg_str, bytes_length)
            _EvisionConsoleLogInfo(msg_str, bytes_length)
            pass

        @staticmethod
        def warning(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogWarning(msg_str, bytes_length)
            _EvisionConsoleLogWarning(msg_str, bytes_length)
            pass

        @staticmethod
        def error(msg):
            msg_str, bytes_length = EvisionLog.convert_str(msg)
            _EvisionFileLogError(msg_str, bytes_length)
            _EvisionConsoleLogError(msg_str, bytes_length)
            pass


# this is a test case
if __name__ == '__main__':
    EvisionLog.init_logger('D:/WorkSpace/EvisionLight')
    EvisionLog.Console.debug("调试调试")
    EvisionLog.Console.info("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    EvisionLog.Console.warning("调试信息")
    EvisionLog.Console.error("调试信息")

    EvisionLog.File.debug("调试调试")
    EvisionLog.File.info("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    EvisionLog.File.warning("调试信息")
    EvisionLog.File.error("调试信息")