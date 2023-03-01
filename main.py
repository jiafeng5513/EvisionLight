import os
import sys
import PySide2
from EvisionLog.EvisionLog import *
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from EvisionSandbox.sandbox_ctl import SandBox

root_path = os.path.dirname(__file__)
sys.path.append(root_path)

if __name__ == '__main__':
    repo_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    EvisionLog.init_logger('./logs')

    dirname = os.path.dirname(PySide2.__file__)
    current_platform = sys.platform
    if current_platform == 'win32':
        plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    elif current_platform == 'linux':
        plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
    else:
        raise RuntimeError("EvisionLight Now only support win32 and linux, but try to start on {}.".format(current_platform))
    EvisionLog.All.info("start on {}".format(current_platform))
    # set up qt runtime env
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

    XDG_CURRENT_DESKTOP = os.environ['XDG_CURRENT_DESKTOP']
    if (XDG_CURRENT_DESKTOP.find('GNOME') != -1) or (XDG_CURRENT_DESKTOP.find('gnome') != -1):
        os.environ['QT_QPA_PLATFORM'] = 'wayland'
    # start main procedure
    app = QApplication([])
    app.setWindowIcon(QIcon("EvisionSandbox/resources/Evision.ico"))  # 添加图标
    sandbox = SandBox()
    sandbox.show()
    app.exec_()
