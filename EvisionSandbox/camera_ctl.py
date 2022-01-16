from PySide2.QtCore import Slot
from PySide2.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PySide2.QtWidgets import QWidget
from EvisionSandbox.camera_ui import Ui_Form


class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        availableCameras = QCameraInfo.availableCameras()
        id = 0
        for cameraInfo in availableCameras:
            self.ui.comboBox_CameraDevice.addItem("{}-{}".format(id, cameraInfo.description()), cameraInfo)
            id += 1
        self.ui.lcdNumber.display(0)
        self.ui.pushButton_CameraOn.setEnabled(False)
        self.ui.pushButton_CameraOff.setEnabled(True)
        # self.m_pCamera = QCamera()
        # self.m_pImageCapture = QCameraImageCapture()
        self.setCamera(QCameraInfo(self.ui.comboBox_CameraDevice.currentData()))

    def setCamera(self, cameraInfo):
        self.m_pCamera = QCamera(cameraInfo)
        self.m_pImageCapture = QCameraImageCapture(self.m_pCamera.metaData(self))
        self.refreshResAndCodecList()
        self.m_pCamera.setCaptureMode(QCamera.CaptureStillImage)
        self.m_pCamera.setCaptureMode(QCamera.CaptureMode.CaptureViewfinder)
        self.m_pCamera.setViewfinder(self.ui.viewfinder)
        self.m_pCamera.start()
        pass

    def refreshResAndCodecList(self):

        pass

    @Slot()
    def on_open_camera(self):
        # setCamera(static_cast < QCameraInfo * > (ui.comboBox_CameraDevice->currentData().data()));
        # ui.pushButton_CameraOn->setEnabled(false);
        # ui.pushButton_CameraOff->setEnabled(true);
        # ui.pushButton_Focus->setEnabled(true);
        # ui.pushButton_Shot->setEnabled(true);
        # ui.horizontalSlider_exposureCompensation->setEnabled(true);
        # ui.horizontalSlider_Quality->setEnabled(true);


        pass

    @Slot()
    def on_close_camera(self):
        pass

    @Slot()
    def on_close_camera(self):
        pass
