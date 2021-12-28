# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sandbox.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resProxy_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1041, 684)
        self.actionCamera = QAction(MainWindow)
        self.actionCamera.setObjectName(u"actionCamera")
        icon = QIcon()
        icon.addFile(u":/sandbox/camera.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionCamera.setIcon(icon)
        self.actionMono_kaliba = QAction(MainWindow)
        self.actionMono_kaliba.setObjectName(u"actionMono_kaliba")
        icon1 = QIcon()
        icon1.addFile(u":/sandbox/MonoKaliba.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionMono_kaliba.setIcon(icon1)
        self.actionStereo_kaliba = QAction(MainWindow)
        self.actionStereo_kaliba.setObjectName(u"actionStereo_kaliba")
        icon2 = QIcon()
        icon2.addFile(u":/sandbox/StereoKaliba.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStereo_kaliba.setIcon(icon2)
        self.actionParallax = QAction(MainWindow)
        self.actionParallax.setObjectName(u"actionParallax")
        icon3 = QIcon()
        icon3.addFile(u":/sandbox/Parallax.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionParallax.setIcon(icon3)
        self.actionDepth_map = QAction(MainWindow)
        self.actionDepth_map.setObjectName(u"actionDepth_map")
        icon4 = QIcon()
        icon4.addFile(u":/sandbox/Heatmap.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDepth_map.setIcon(icon4)
        self.actionPoint_Cloud_Viever = QAction(MainWindow)
        self.actionPoint_Cloud_Viever.setObjectName(u"actionPoint_Cloud_Viever")
        icon5 = QIcon()
        icon5.addFile(u":/sandbox/CloudViewer.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPoint_Cloud_Viever.setIcon(icon5)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")

        self.gridLayout.addWidget(self.mdiArea, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1041, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menu.addAction(self.actionCamera)
        self.menu_2.addAction(self.actionMono_kaliba)
        self.menu_2.addAction(self.actionStereo_kaliba)
        self.menu_2.addAction(self.actionParallax)
        self.menu_2.addAction(self.actionDepth_map)
        self.menu_3.addAction(self.actionPoint_Cloud_Viever)
        self.menuHelp.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionCamera)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMono_kaliba)
        self.toolBar.addAction(self.actionStereo_kaliba)
        self.toolBar.addAction(self.actionParallax)
        self.toolBar.addAction(self.actionDepth_map)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPoint_Cloud_Viever)

        self.retranslateUi(MainWindow)
        self.actionCamera.triggered.connect(MainWindow.on_open_camera_view)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EvisionLight", None))
        self.actionCamera.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.actionMono_kaliba.setText(QCoreApplication.translate("MainWindow", u"Mono Kaliba", None))
        self.actionStereo_kaliba.setText(QCoreApplication.translate("MainWindow", u"Stereo Kaliba", None))
        self.actionParallax.setText(QCoreApplication.translate("MainWindow", u"Parallax", None))
        self.actionDepth_map.setText(QCoreApplication.translate("MainWindow", u"Depth Map Tool", None))
        self.actionPoint_Cloud_Viever.setText(QCoreApplication.translate("MainWindow", u"Point Cloud Viever", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"2D-Vision", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"3D-Vision", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

