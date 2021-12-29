from PySide2.QtWidgets import QWidget
from ui.camera_ui import Ui_Form


class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)