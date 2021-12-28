# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtMultimediaWidgets import QCameraViewfinder
from PySide2.QtWidgets import *




class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1108, 729)
        self.gridLayout_6 = QGridLayout(Form)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_FindSavePath = QPushButton(self.frame_4)
        self.pushButton_FindSavePath.setObjectName(u"pushButton_FindSavePath")

        self.horizontalLayout_3.addWidget(self.pushButton_FindSavePath)

        self.lineEdit_SavePath = QLineEdit(self.frame_4)
        self.lineEdit_SavePath.setObjectName(u"lineEdit_SavePath")
        self.lineEdit_SavePath.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEdit_SavePath)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.lcdNumber = QLCDNumber(self.frame_4)
        self.lcdNumber.setObjectName(u"lcdNumber")

        self.horizontalLayout_3.addWidget(self.lcdNumber)


        self.gridLayout_6.addWidget(self.frame_4, 0, 0, 1, 2)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.viewfinder = QCameraViewfinder(self.frame_2)
        self.viewfinder.setObjectName(u"viewfinder")
        self.viewfinder.setAutoFillBackground(True)

        self.gridLayout_5.addWidget(self.viewfinder, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_2, 1, 0, 7, 1)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(200, 16777215))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_CameraOn = QPushButton(self.frame)
        self.pushButton_CameraOn.setObjectName(u"pushButton_CameraOn")
        self.pushButton_CameraOn.setMinimumSize(QSize(0, 0))
        self.pushButton_CameraOn.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.pushButton_CameraOn, 0, 0, 1, 1)

        self.pushButton_CameraOff = QPushButton(self.frame)
        self.pushButton_CameraOff.setObjectName(u"pushButton_CameraOff")
        self.pushButton_CameraOff.setEnabled(True)
        self.pushButton_CameraOff.setMinimumSize(QSize(0, 0))
        self.pushButton_CameraOff.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.pushButton_CameraOff, 0, 1, 1, 1)

        self.pushButton_Focus = QPushButton(self.frame)
        self.pushButton_Focus.setObjectName(u"pushButton_Focus")
        self.pushButton_Focus.setEnabled(True)
        self.pushButton_Focus.setMinimumSize(QSize(0, 0))
        self.pushButton_Focus.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.pushButton_Focus, 1, 0, 1, 1)

        self.pushButton_Shot = QPushButton(self.frame)
        self.pushButton_Shot.setObjectName(u"pushButton_Shot")
        self.pushButton_Shot.setEnabled(True)
        self.pushButton_Shot.setMinimumSize(QSize(0, 0))
        self.pushButton_Shot.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.pushButton_Shot, 1, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(200, 16777215))
        self.groupBox_2.setFlat(True)
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSlider_exposureCompensation = QSlider(self.groupBox_2)
        self.horizontalSlider_exposureCompensation.setObjectName(u"horizontalSlider_exposureCompensation")
        self.horizontalSlider_exposureCompensation.setEnabled(True)
        self.horizontalSlider_exposureCompensation.setMinimumSize(QSize(170, 0))
        self.horizontalSlider_exposureCompensation.setMaximumSize(QSize(170, 16777215))
        self.horizontalSlider_exposureCompensation.setContextMenuPolicy(Qt.NoContextMenu)
        self.horizontalSlider_exposureCompensation.setMinimum(-4)
        self.horizontalSlider_exposureCompensation.setMaximum(4)
        self.horizontalSlider_exposureCompensation.setPageStep(2)
        self.horizontalSlider_exposureCompensation.setOrientation(Qt.Horizontal)
        self.horizontalSlider_exposureCompensation.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout.addWidget(self.horizontalSlider_exposureCompensation)


        self.gridLayout_6.addWidget(self.groupBox_2, 2, 1, 1, 1)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(200, 16777215))
        self.groupBox_3.setFlat(True)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSlider_Quality = QSlider(self.groupBox_3)
        self.horizontalSlider_Quality.setObjectName(u"horizontalSlider_Quality")
        self.horizontalSlider_Quality.setEnabled(True)
        self.horizontalSlider_Quality.setMinimumSize(QSize(170, 0))
        self.horizontalSlider_Quality.setMaximumSize(QSize(170, 16777215))
        self.horizontalSlider_Quality.setContextMenuPolicy(Qt.NoContextMenu)
        self.horizontalSlider_Quality.setOrientation(Qt.Horizontal)
        self.horizontalSlider_Quality.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout_2.addWidget(self.horizontalSlider_Quality)


        self.gridLayout_6.addWidget(self.groupBox_3, 3, 1, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(200, 16777215))
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox_CameraDevice = QComboBox(self.groupBox)
        self.comboBox_CameraDevice.setObjectName(u"comboBox_CameraDevice")
        self.comboBox_CameraDevice.setMinimumSize(QSize(170, 0))
        self.comboBox_CameraDevice.setMaximumSize(QSize(170, 16777215))

        self.gridLayout_2.addWidget(self.comboBox_CameraDevice, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 4, 1, 1, 1)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(200, 16777215))
        self.groupBox_4.setFlat(True)
        self.gridLayout_3 = QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBox_Resolution = QComboBox(self.groupBox_4)
        self.comboBox_Resolution.setObjectName(u"comboBox_Resolution")
        self.comboBox_Resolution.setMinimumSize(QSize(170, 0))
        self.comboBox_Resolution.setMaximumSize(QSize(170, 16777215))

        self.gridLayout_3.addWidget(self.comboBox_Resolution, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_4, 5, 1, 1, 1)

        self.groupBox_5 = QGroupBox(Form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(200, 16777215))
        self.groupBox_5.setFlat(True)
        self.gridLayout_4 = QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.comboBox_Codec = QComboBox(self.groupBox_5)
        self.comboBox_Codec.setObjectName(u"comboBox_Codec")
        self.comboBox_Codec.setMinimumSize(QSize(170, 0))
        self.comboBox_Codec.setMaximumSize(QSize(170, 16777215))

        self.gridLayout_4.addWidget(self.comboBox_Codec, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_5, 6, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 273, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 7, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Camera", None))
        self.pushButton_FindSavePath.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u5230", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8ba1\u6570\u5668:", None))
        self.pushButton_CameraOn.setText(QCoreApplication.translate("Form", u"\u6444\u50cf\u673a\u5f00", None))
        self.pushButton_CameraOff.setText(QCoreApplication.translate("Form", u"\u6444\u50cf\u673a\u5173", None))
        self.pushButton_Focus.setText(QCoreApplication.translate("Form", u"Focus", None))
        self.pushButton_Shot.setText(QCoreApplication.translate("Form", u"\u62cd\u7167", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u66dd\u5149\u8865\u507f", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u56fe\u7247\u8d28\u91cf", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u6444\u50cf\u5934", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u5206\u8fa8\u7387", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"\u56fe\u7247\u683c\u5f0f", None))
    # retranslateUi

