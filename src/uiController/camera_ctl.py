from PySide2.QtWidgets import QWidget
from src.ui.camera import Ui_Form


class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)