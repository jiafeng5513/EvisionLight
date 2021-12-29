from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow
from ui.sandbox_ui import Ui_MainWindow
from uiController.camera_ctl import Camera


class SandBox(QMainWindow):
    def __init__(self):
        super(SandBox, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @Slot()
    def on_open_camera_view(self):
        camera = Camera()
        self.ui.mdiArea.addSubWindow(camera)
        camera.show()