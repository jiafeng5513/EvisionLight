# -*- coding: UTF-8 -*-
import glob
import os
import subprocess
import sys
import PySide2
from EvisionLog.EvisionLog import *
repo_dir = os.path.abspath("../")


def uic(uic_exe, ui_files):
    for ui_file in ui_files:
        ui_py_filename = ui_file.replace('.ui', '_ui.py')
        subprocess.call("{} {} -o {} -g python".format(uic_exe, ui_file, ui_py_filename), env=envs, shell=True)
        print("uic {}".format(ui_file))


def qrc(rcc_exe, qrc_files):
    for qrc_file in qrc_files:
        rc_py_filename = qrc_file.replace('.qrc', '_rc.py')
        subprocess.call("{} {} -o {} -g python".format(rcc_exe, qrc_file, rc_py_filename), env=envs, shell=True)
        print("qrc {}".format(qrc_file))


if __name__ == '__main__':
    dirname = os.path.dirname(PySide2.__file__)
    current_platform = sys.platform
    if current_platform == 'win32':
        plugin_path = os.path.join(dirname, 'plugins', 'platforms')
        uic_exe_path = os.path.join(dirname, 'uic.exe')
        rcc_exe_path = os.path.join(dirname, 'rcc.exe')
        envs = {'QT_QPA_PLATFORM_PLUGIN_PATH': plugin_path, 'PATH': r"C:\windows\system32"}
    elif current_platform == 'linux':
        plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
        uic_exe_path = os.path.join(dirname, 'uic')
        rcc_exe_path = os.path.join(dirname, 'rcc')
        envs = {'QT_QPA_PLATFORM_PLUGIN_PATH': plugin_path}
    else:
        raise RuntimeError(
            "EvisionLight Now only support win32 and linux, but try to start on {}.".format(current_platform))

    print("start on {}".format(current_platform))
    print("PySide2 plugin path = {}".format(plugin_path))
    print("PySide2 uic path = {}".format(uic_exe_path))
    print("PySide2 rcc path = {}".format(rcc_exe_path))

    # set up qt runtime env
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    ui_file_list = []
    qrc_file_list = []

    for root, dirnames, filenames in os.walk(repo_dir):
        for filename in filenames:
            if filename.endswith(".ui"):
                ui_file_list.append(os.path.join(root, filename))
            if filename.endswith(".qrc"):
                qrc_file_list.append(os.path.join(root, filename))

    uic(uic_exe_path, ui_file_list)
    qrc(rcc_exe_path, qrc_file_list)







