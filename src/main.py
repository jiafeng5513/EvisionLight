import os
import sys
import PySide2

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from front.uiController.sandbox_ctl import SandBox

if __name__ == '__main__':
    dirname = os.path.dirname(PySide2.__file__)
    current_platform = sys.platform
    if current_platform == 'win32':
        plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    elif current_platform == 'linux':
        plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
    else:
        raise RuntimeError("EvisionLight Now only support win32 and linux, but try to start on {}.".format(current_platform))

    # set up qt runtime env
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

    # start main procedure
    app = QApplication([])
    app.setWindowIcon(QIcon("front/ui/resources/Evision.ico"))  # 添加图标
    sandbox = SandBox()
    sandbox.show()
    app.exec_()
