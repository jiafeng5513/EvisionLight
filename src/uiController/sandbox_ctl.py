from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow
from src.ui.sandbox import Ui_MainWindow
from src.uiController.camera_ctl import Camera


class SandBox(QMainWindow):
    def __init__(self):
        super(SandBox, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @Slot()
    def on_open_camera_view(self):
        """在控制台输出内容"""
        print("Button clicked")
        camera = Camera()
        self.ui.mdiArea.addSubWindow(camera)
        camera.show()