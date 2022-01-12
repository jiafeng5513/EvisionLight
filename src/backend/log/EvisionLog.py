import os
import sys
from ctypes import *

current_platform = sys.platform
if current_platform == 'win32':
    EvisionLogLibrary = cdll.LoadLibrary('../../../install/EvisionLog.dll')
else:
    EvisionLogLibrary = cdll.LoadLibrary('../../../install/EvisionLog.so')

_EvisionLogInit = EvisionLogLibrary.EvisionLogInit
_EvisionConsoleLogInfo = EvisionLogLibrary.EvisionConsoleLogInfo
_EvisionConsoleLogInfo.argtypes = [c_wchar_p, c_int]


def Log_init():
    _EvisionLogInit()


def Log_info_to_console(msg):
    # STR = (c_wchar * 100)(*bytes("123456768", 'utf-8'))  # 把一组100个的字符定义为STR
    # cast(STR, POINTER(c_wchar))
    msg_bytes = bytes(msg, 'utf-8')
    length = len(msg_bytes)
    p = c_wchar_p(msg)
    # msg_str = (c_wchar * length)(*bytes(msg, 'utf-8'))
    _EvisionConsoleLogInfo(c_wchar_p(msg), 2*length)
    pass

if __name__ == '__main__':
    Log_init()
    Log_info_to_console("这是什么")
    Log_info_to_console("123456768ab")
    Log_info_to_console("123456768abc")