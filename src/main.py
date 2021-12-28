import sys, os
import PySide2
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from uiController.sandbox_ctl import SandBox





if __name__ == '__main__':
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    print("PySide2 plugin path = {}".format(plugin_path))
    uic_exe_path = os.path.join(dirname, 'uic.exe')
    print("PySide2 uic path = {}".format(uic_exe_path))
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/Evision.ico"))  # 添加图标
    sandbox = SandBox()
    sandbox.show()

    app.exec_()
