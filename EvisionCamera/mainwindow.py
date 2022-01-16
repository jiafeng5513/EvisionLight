#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a window for displaying frame and its properties

The main companent of usbcamGUI consists of main window with PySide2. Frame from
camera are shown on the windows.
"""
import re
import subprocess
import numpy as np
import platform
from pathlib import Path
from datetime import datetime
from typing import Callable
from PIL import Image

from PySide2.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QWidget, QAction,
    QPushButton, QMenu, QMenuBar, QVBoxLayout, QHBoxLayout, QStatusBar, QGridLayout,
    QMessageBox, QScrollArea, QLabel, QFrame, QTableWidget, QTableWidgetItem, QInputDialog, QDialog,
    QAbstractItemView, QSizePolicy, QFileDialog, QAbstractScrollArea, QGroupBox,
    QGraphicsPixmapItem, QSlider, QFontDialog, QDialogButtonBox, QToolBar, QSpinBox, QComboBox,
    QFontComboBox, QRadioButton, QButtonGroup, QCheckBox, QTextEdit
    )
from PySide2.QtGui import QIcon, QPixmap, QImage
from PySide2.QtCore import Qt, QTimer, QIODevice

from camera import LinuxCamera, WindowsCamera, RaspiCamera
from text import MessageText
from icon import Icon
from slot import Slot
from fileIO import FileIO
from util import Utility
import breeze_resources


class Window(QMainWindow):
    """Class to create main widnow

    Creates main window for displaying frame read from a connected camera.
    The main window contains memu bar, tool bar, status bar, sliders and the
    boxes showing the camera's information. These widget are created and added to
    main window in the instance method of this class.

    """
    def __init__(
            self, device: int = 0, suffix: str = "png", camtype: str = "usb_cam",
            color: str = "RGB", dst: str = ".", param: str = "full",
            rule: str = "Sequential", parent=None):
        super(Window, self).__init__(parent)
        self.device = device
        self.camtype = camtype
        self.colorspace = color
        self.image_suffix = suffix
        self.video_codec = "AVC1"
        self.video_suffix = "avi"
        self.dst = Path(dst)
        self.parent_dir = Path(__file__).parent.resolve()

        self.filename_rule_lst = FileIO.file_save
        self.filename_rule = FileIO.file_save_lst[-1]

        self.is_display = True
        self.param_separate = False

        self.slot = Slot(self)

        cam = self.get_cam()
        self.camera = cam(self.device, self.colorspace, parent=self)
        self.support_params = self.camera.get_supported_params()
        self.current_params = self.camera.get_current_params(param)

        # List of camera properties with temporal initial values
        self.prop_table = [
            ["Fourcc", "aa"],
            ["Width", 640],
            ["Height", 480],
            ["FPS", 30.0],
            ["Bit depth", 8],
            ["File naming style", self.filename_rule]
        ]
        self.setup()
        self.set_timer()

    def get_cam(self) -> str:
        """Return camera object according to current OS.

        Detects what OS you are using, return camera objects  in order to function properly.

            - Linux: LinuxCamera
            - RaspberryPi OS: RaspiCamera
            - Windows: WindowsCamera

        Returns:
            Camera class
        """
        if self.camtype == "raspi":
            return RaspiCamera

        self.system = platform.system()
        if re.search("linux", self.system, re.IGNORECASE):
            return LinuxCamera
        elif re.search("windows", self.system, re.IGNORECASE):
            return WindowsCamera
        else:
            return "Unknown type"

    def setup(self):
        """Setup the main window for displaying frame and widget.

        Creates a QMainWindow object, then add menubar, toolbar, statusbar, widgets and layout
        into the window.
        """
        self.setFocusPolicy(Qt.ClickFocus)
        self.setContentsMargins(20, 0, 20, 0)
        self.information_window_setup()
        self.view_setup()
        self.layout_setup()
        self.image_setup()
        self.toolbar_setup()
        self.setWindowTitle("usbcamGUI")
        self.update_prop_table()
        self.adjust_windowsize()
        self.set_theme()

    def adjust_windowsize(self):
        """Adjusts the main window size
        """
        system = Utility.get_os()
        if system == "linux":
            w, h, _ = self.get_screensize()
            wscale = 0.5
            hscale = 0.7
            self.resize(wscale * w, hscale * h)
        else:
            self.resize(800, 600)

    def set_theme(self):
        """Set color theme of the main window.
        """
        self.style_theme = "light"
        self.style_theme_sheet = ":/{}.qss".format(self.style_theme)
        self.slot.switch_theme()
        self.set_font(self.camera.font_family, self.camera.font_size)

    def set_font(self, family: str = "Yu Gothic", size: int = 14):
        """Sets font-family and size of UI.

        Args:
            family (str, optional): Font-family. Defaults to "Yu Gothic".
            size (int, optional): Font-size. Defaults to 20.
        """
        self.setStyleSheet('font-family: "{}"; font-size: {}px;'.format(family, size))

    def set_timer(self):
        """Set QTimer

        Creates a QTimer object to update frame on view area. The interval is set to the inverse
        of camera FPS.
        """
        self.qtime_factor = 0.8
        self.fps = 30.0
        if self.fps:
            self.msec = 1 / self.fps * 1000 * self.qtime_factor
        else:
            self.msec = 1 / 30.0 * 1000 * self.qtime_factor
        self.timer = QTimer()
        self.timer.setInterval(self.msec)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start()

    def stop_timer(self):
        """Deactivate the Qtimer object.
        """
        self.timer.stop()

    def start_timer(self):
        """Activate the Qtimer object.
        """
        self.fps = 30.0
        if self.fps:
            self.msec = 1 / self.fps * 1000 * self.qtime_factor
        else:
            self.msec = 1 / 30.0 * 1000 * self.qtime_factor
        self.timer.setInterval(self.msec)
        self.timer.start()

    def toolbar_setup(self):
        """Create toolbar
        """
        self.toolbar = QToolBar("test", self)
        self.addToolBar(self.toolbar)

        current_size = str(self.font().pointSize())
        lst = [str(i) for i in range(6, 14)]
        lst.extend([str(i) for i in range(14, 40, 2)])
        index = lst.index(current_size)

        self.fontsize_combo = QComboBox()
        self.fontsize_combo.addItems(lst)
        self.fontsize_combo.setCurrentIndex(index)
        self.fontsize_combo.currentTextChanged.connect(self.slot.set_fontsize)
        self.fontsize_label = QLabel("Font size")
        self.fontsize_label.setFrameShape(QFrame.Box)

        self.comb = QFontComboBox()

        self.toolbar.addWidget(self.save_button)
        self.toolbar.addWidget(self.stop_button)
        self.toolbar.addWidget(self.rec_button)
        self.toolbar.addWidget(self.close_button)
        self.toolbar.addWidget(self.theme_button)
        self.toolbar.addWidget(self.help_button)
        self.toolbar.addWidget(self.fontsize_label)
        self.toolbar.addWidget(self.fontsize_combo)
        self.toolbar.setStyleSheet(
            """
            QToolBar {spacing:5px;}
            """
            )

    def view_setup(self):
        """Set view area to diplay read frame in part of the main window
        """
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.width = 640
        self.height = 480
        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.view.setMouseTracking(True)
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

    def layout_setup(self):
        """Set layout of objects on the window.
        """
        self.window = QWidget()
        self.setCentralWidget(self.window)
        #self.view.mouseMoveEvent = self.get_coordinates

        self.main_layout = QHBoxLayout()
        self.window.setLayout(self.main_layout)

        self.add_actions()
        self.add_menubar()
        self.add_statusbar()
        self.button_block = self.add_buttons()
        self.slider_group = self.add_params()
        self.prop_block = self.add_prop_window()
        self.create_mainlayout()

    def image_setup(self):
        """Creates a Qimage to assign frame, then initialize with an image which has zero in all pixels.
        """
        self.frame = np.zeros((640, 480, 3), dtype=np.uint8)
        #cinit = np.ctypeslib.as_ctypes(self.frame)
        #self.frame.buffer = sharedctypes.RawArray(cinit._type_, cinit)
        self.qimage = QImage(
            self.frame.data,
            640,
            480,
            640 * 3,
            QImage.Format_RGB888
            )
        self.pixmap = QPixmap.fromImage(self.qimage)

    def add_actions(self):
        """Add actions executed when press each item in the memu window.
        """
        self.save_act = self.create_action("&Save", self.save_frame, "Ctrl+s")
        self.stop_act = self.create_action("&Pause", self.stop_frame, "Ctrl+p", checkable=True)
        self.rec_act = self.create_action("&Record", self.record, "Ctrl+r", True)
        self.quit_act = self.create_action("&Quit", self.slot.quit, "Ctrl+q")

        self.theme_act = self.create_action("Switch &Theme", self.slot.switch_theme, "Ctrl+t")
        self.param_act = self.create_action("Choose parameter slider", self.slot.switch_paramlist, "Ctrl+g")
        self.show_paramlist_act = self.create_action("Parameters &List", self.slot.show_paramlist, "Ctrl+l")
        self.show_shortcut_act = self.create_action("&Keybord shortcut", self.slot.show_shortcut, "Ctrl+k")
        self.font_act = self.create_action("&Font", self.slot.set_font, "Ctrl+f")

        self.usage_act = self.create_action("&Usage", self.slot.usage, "Ctrl+h")
        self.about_act = self.create_action("&About", self.slot.about, "Ctrl+a")

    def create_action(self, text: str, slot: Callable, key: str = None, checkable: bool = False,
        check_defalut: bool = False) -> QAction:
        """Create a QAction object.

        Args:
            text (str): Text shown on menu.
            slot (Callable): A method called when click the menu.
            key (str, optional): Shortcut key. Defaults to None.
            checkable (bool, optional): Add a checkbox into the menu. Defaults to False.
            check_defalut (bool, optional): Check default status. Defaults to False.

        Returns:
            QAction: PySide2 QAction
        """
        act = QAction(text)
        act.setShortcut(key)
        if checkable:
            act.setCheckable(True)
            act.setChecked(check_defalut)
            act.toggled.connect(slot)
        else:
            act.triggered.connect(slot)

        return act

    def add_menubar(self):
        """Create menu bar, then add to the main window.
        """
        self.menubar = QMenuBar()
        self.setMenuBar(self.menubar)

        self.file_tab = QMenu("&File")
        self.file_tab.addAction(self.save_act)
        self.file_tab.addAction(self.stop_act)
        self.file_tab.addAction(self.rec_act)
        self.file_tab.addSeparator()
        self.file_tab.addAction(self.quit_act)
        #self.file_tab.setSizePolicy(policy)

        self.view_tab = QMenu("&View")
        self.view_tab.addAction(self.theme_act)
        self.view_tab.addAction(self.font_act)
        self.view_tab.addAction(self.param_act)
        self.view_tab.addAction(self.show_shortcut_act)
        self.view_tab.addAction(self.show_paramlist_act)

        self.help_tab = QMenu("&Help")
        self.help_tab.addAction(self.usage_act)
        self.help_tab.addAction(self.about_act)

        self.menubar.addMenu(self.file_tab)
        self.menubar.addMenu(self.view_tab)
        self.menubar.addMenu(self.help_tab)
        self.menubar.setStyleSheet(
            """
            QMenuBar {
                    font-size: 16px;
                    spacing:10px;
                    padding-top: 5px;
                    padding-bottom: 10px;
                }
            """
            )

    def add_statusbar(self):
        """Create status bar, then add to the main window.

        The status bar shows the coordinates on the frame where the cursor is located and
        its pixel value. The pixel value has RGB if the format of is color (RGB), does grayscale
        value if grayscale.
        """
        self.statbar_list = []
        if self.colorspace == "rgb":
            self.stat_css = {
                "postion": "color: white",
                "R": "color: white;",
                "G": "color: white;",
                "B": "color: white;",
                "alpha": "color: white;",
            }
        else:
            self.stat_css = {
                "postion": "color: black;",
                "gray": "color: black"
            }

        for s in self.stat_css.values():
            stat = QStatusBar(self)
            stat.setStyleSheet(s)
            self.statbar_list.append(stat)

        first = True
        for stat in self.statbar_list:
            if first:
                self.setStatusBar(stat)
                self.statbar_list[0].reformat()
                first = False
            else:
                self.statbar_list[0].addPermanentWidget(stat)

    def add_buttons(self):
        """Add push buttons on the window.

        Add quit, save stop and usage buttons on the windows. When press each button, the set
        method (called "slot" in Qt framework) are execeuted.
        """
        self.save_button = self.create_button("&Save", self.save_frame, None, None, "Save the frame")
        self.stop_button = self.create_button("&Pause", self.stop_frame, None, None, "Stop reading frame", True)
        self.rec_button = self.create_button("&Rec", self.record, None, None, "Start recording", True)
        self.close_button = self.create_button("&Quit", self.slot.quit, None, None, "Quit the program")
        self.theme_button = self.create_button("Light", self.slot.switch_theme, None, None, "Switche color theme")
        self.help_button = self.create_button("&Usage", self.slot.usage, None, None, "Show usage")

        self.frame_button = self.create_button(
            "Properties",
            self.slot.change_frame_prop,
            None,
            tip="Change properties",
            minsize=(150, 30)
            )
        self.default_button = self.create_button(
            "&Default params",
            self.set_param_default,
            "Ctrl+d",
            tip="Set default parameters",
            minsize=(150, 30)
            )
        self.filerule_button = self.create_button(
            "&Naming style",
            self.slot.set_file_rule,
            "Ctrl+n",
            tip="Change naming style",
            minsize=(150, 30)
            )

        hbox = QHBoxLayout()
        hbox.addWidget(self.save_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.rec_button)
        hbox.addWidget(self.close_button)
        hbox.addWidget(self.theme_button)
        hbox.addWidget(self.help_button)
        return hbox

    def create_button(self, text: str, slot: Callable, key: str = None, icon: Icon = None,
        tip: str = None, checkable: bool = False, minsize: tuple = None) -> QPushButton:
        """Create a QPushButton object.

        Args:
            text (str): Text shown on the button.
            slot (Callable): A method called when click the button.
            key (str, optional): Shortcut key. Defaults to None.
            icon (Icon, optional): An icon shown on the button. Defaults to None.
            tip (str, optional): A tips shown when position the pointer on the button. Defaults to None.
            checkable (bool, optional): Add button to checkbox. Defaults to False.
            msize (tuple, optional): Minimum size of the button box, (width, height).

        Returns:
            QPushButton: PySide2 QPushButton
        """
        button = QPushButton(text)
        if checkable:
            button.setCheckable(True)
            button.toggled.connect(slot)
        else:
            button.clicked.connect(slot)

        if key:
            button.setShortcut(key)
        if icon:
            button.setIcon(QIcon(icon))
        if tip:
            button.setToolTip(tip)
        if minsize:
            button.setMinimumSize(minsize[0], minsize[1])
        else:
            button.setMinimumSize(80, 30)
        return button

    def add_params(self) -> QGridLayout:
        """Set the properties of camera parameter.

        Set the properties of camera parameter, then add sliders to change each parameter.
        When change value on the slider, the value of paramter also changes by the caller
        function.

        """
        lst = self.current_params
        for key, value in lst.items():
            self.add_slider(key)

        # add sliders
        self.slider_table = QGridLayout()
        self.slider_table.setSpacing(15)
        self.slider_table.setContentsMargins(20, 20, 20, 20)
        for row, param in enumerate(self.current_params):
            self.slider_table.addWidget(self.current_params[param]["slider_label"], row, 0)
            self.slider_table.addWidget(self.current_params[param]["slider"], row, 1)
            self.slider_table.addWidget(self.current_params[param]["slider_value"], row, 2)
        if len(self.current_params) > 15:
            self.param_separate = True
        else:
            self.param_separate = False
        return self.slider_table

    def update_params(self, plist: list) -> QGridLayout:
        """Update camera's paramters and sliders shown on the windows.
        """
        #self.current_params.clear()
        self.current_params = self.camera.get_current_params("selected", plist)
        for key, value in self.current_params.items():
            self.add_slider(key)

        # add sliders
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        for row, param in enumerate(self.current_params):
            grid.addWidget(self.current_params[param]["slider_label"], row, 0)
            grid.addWidget(self.current_params[param]["slider"], row, 1)
            grid.addWidget(self.current_params[param]["slider_value"], row, 2)
        if len(self.current_params) > 15:
            self.param_separate = True
        else:
            self.param_separate = False
        self.slider_group = grid
        self.update_mainlayout()
        self.update_prop_table()
        self.write_text("update sliders")
        return grid

    def add_slider(self, param: str):
        """Creates slider, labels to show pamarater's name and its value.

        Args:
            param (str): A parameter to create slider.
        """
        min_ = self.current_params[param]["min"]
        max_ = self.current_params[param]["max"]
        step = self.current_params[param]["step"]
        value = self.current_params[param]["value"]

        slider = QSlider(Qt.Horizontal)
        if max_:
            slider.setRange(min_, max_)
        else:
            slider.setRange(0, 1)
        slider.setValue(int(value))
        slider.setTickPosition(QSlider.TicksBelow)
        slider.valueChanged.connect(lambda val, p=param: self.set_sliderval(p, val))

        if step:
            if max_ < 5:
                slider.setTickInterval(step)
            else:
                slider.setTickInterval(10)

        slider_label = QLabel(param)
        slider_value = QLabel(str(value))

        slider_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        slider_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.current_params[param]["slider"] = slider
        self.current_params[param]["slider_label"] = slider_label
        self.current_params[param]["slider_value"] = slider_value

    def add_prop_window(self) -> QGridLayout:
        """Create a table to show the current properties of camera.

        Returns:
            QGridLayout: PySide2 QGridLayout
        """
        header = ["property", "value"]
        self.prop_table_widget = QTableWidget(self)
        self.prop_table_widget.setColumnCount(len(header))
        self.prop_table_widget.setRowCount(len(self.prop_table))

        self.prop_table_widget.setHorizontalHeaderLabels(header)
        self.prop_table_widget.verticalHeader().setVisible(False)
        self.prop_table_widget.setAlternatingRowColors(True)
        self.prop_table_widget.horizontalHeader().setStretchLastSection(True)
        self.prop_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.prop_table_widget.setFocusPolicy(Qt.NoFocus)

        for row, content in enumerate(self.prop_table):
            for col, elem in enumerate(content):
                self.item = QTableWidgetItem(elem)

                self.prop_table_widget.setItem(row, col, self.item)
        self.prop_table_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #self.prop_table_widget.resizeColumnsToContents()
        #self.prop_table_widget.resizeRowsToContents()
        self.prop_table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.prop_table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.prop_table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.prop_table_widget.setColumnWidth(0, 150)
        self.prop_table_widget.setColumnWidth(1, 150)

        vbox = QVBoxLayout()
        vbox.addWidget(self.prop_table_widget)
        vbox.setContentsMargins(20, 20, 20, 20)
        self.prop_group = QGroupBox("Frame Properties")
        self.prop_group.setLayout(vbox)
        return self.prop_group

    def information_window_setup(self):
        """Creates information window.

        Creates the information window where the event related to camera or window.
        """
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.show()
        vbox = QVBoxLayout()
        vbox.addWidget(self.text_edit)
        self.text_edit_box = QGroupBox("Information", self)
        self.text_edit_box.setLayout(vbox)
        self.text_edit_box.setAlignment(Qt.AlignLeft)

    def create_mainlayout(self):
        """Create the main layout which consists of view area and information window.
        """
        self.main_layout.addLayout(self.create_view_area_layout())
        self.main_layout.addLayout(self.create_information_layout())

    def update_mainlayout(self):
        """Recreate the main layout.
        """
        self.delete_layout(self.information_layout)
        self.delete_layout(self.upper_right)
        self.add_prop_window()
        self.main_layout.addLayout(self.create_information_layout())

    def delete_layout(self, layout):
        """Delete layout

        Args:
            layout (QBoxLayout): QBoxLayout class object to delete
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            try:
                child.spacerIitem().deleteLater()
            except:
                pass

    def create_view_area_layout(self) -> QVBoxLayout:
        """Creates view area layout
        """
        self.view_area_layout = QVBoxLayout()
        self.view_area_layout.addWidget(self.view, 2)
        self.view_area_layout.addWidget(self.text_edit_box)
        return self.view_area_layout

    def create_information_layout(self):
        """Creates information part layout

        upper-left: current properties
        upper-right: buttons
        lower: sliders
        """
        if self.param_separate:
            self.entry_box = QVBoxLayout()
            self.entry_box.addWidget(self.frame_button)
            self.entry_box.addWidget(self.filerule_button)
            self.entry_box.addWidget(self.default_button)
            self.entry_box.addStretch(1)
            self.entry_box.setSpacing(20)
            self.entry_box.setContentsMargins(20, 20, 20, 20)

            self.button_group_box = QGroupBox("Buttons", self)
            self.button_group_box.setLayout(self.entry_box)
            self.button_group_box.setAlignment(Qt.AlignLeft)

            self.upper_right = QVBoxLayout()
            self.upper_right.addWidget(self.prop_group, 1)
            self.upper_right.addWidget(self.button_group_box, 1)

            self.slider_group_box = QGroupBox("Parameters")
            self.slider_group_box.setLayout(self.slider_group)
            self.slider_group_box.setContentsMargins(20, 20, 20, 20)

            self.information_layout = QHBoxLayout()
            self.information_layout.addLayout(self.upper_right, 1)
            self.information_layout.addWidget(self.slider_group_box, 2)
            #self.information_layout.addStretch(1)
            return self.information_layout
        else:
            self.entry_box = QVBoxLayout()
            self.entry_box.addWidget(self.frame_button)
            self.entry_box.addWidget(self.filerule_button)
            self.entry_box.addWidget(self.default_button)
            self.entry_box.addStretch(1)
            self.entry_box.setSpacing(20)
            self.entry_box.setContentsMargins(20, 20, 20, 20)

            self.button_group_box = QGroupBox("Buttons", self)
            self.button_group_box.setLayout(self.entry_box)
            self.button_group_box.setAlignment(Qt.AlignLeft)

            self.upper_right = QHBoxLayout()
            self.upper_right.addWidget(self.prop_group)
            self.upper_right.addWidget(self.button_group_box)

            self.slider_group_box = QGroupBox("Parameters")
            self.slider_group_box.setLayout(self.slider_group)
            self.slider_group_box.setContentsMargins(20, 20, 20, 20)

            self.information_layout = QVBoxLayout()
            self.information_layout.addLayout(self.upper_right)
            self.information_layout.addWidget(self.slider_group_box)
            self.information_layout.setSpacing(30)
            return self.information_layout

    # decorator
    def display(func):
        def wrapper(self, *args, **kwargs):
            try:
                self.is_display = False
                self.stop_timer()
                func(self, *args, **kwargs)
            finally:
                self.is_display = True
                self.start_timer()
        return wrapper

    def stop_frame(self, checked: bool):
        """Stop reading next frame.

        Args:
            checked (bool): True when presse the Stop button (toggle on). False when press
                again (toggel off).
        """
        if checked:
            self.write_text("Stop !!")
            self.is_display = False
            self.stop_button.setText('Start')
            self.stop_button.setChecked(True)
            self.stop_act.setText('Start')
            self.stop_act.setChecked(True)
        else:
            self.write_text("Start !!")
            self.is_display = True
            self.stop_button.setText('&Pause')
            self.stop_button.setChecked(False)
            self.stop_act.setText('&Pause')
            self.stop_act.setChecked(False)

    def keyPressEvent(self, event):
        """Exit the program

        This method will be called when press the Escape key on the window.
        """
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    def get_coordinates(self, event):
        """Show the current coordinates and value in the pixel where the cursor is located.

        The status bar is updates by the obtained values.
        """
        if self.item is self.view.itemAt(event.pos()):
            sp = self.view.mapToScene(event.pos())
            lp = self.item.mapFromScene(sp).toPoint()
            (x, y) = lp.x(), lp.y()
            #color = self.frame.image.pixel(x, y)
            color = self.qimage.pixelColor(x, y)
            if self.colorspace == "rgb":
                value = color.getRgb()
            elif self.colorspace == "gray":
                value = color.value()

            # Return none if the coordinates are out of range
            if x < 0 and self.frame.width < x:
                return
            elif y < 0 and self.frame.height < y:
                return

            if self.frame.img_is_rgb:
                status_list = [
                    "( x : {}, y :{} )".format(x, y),
                    "R : {}".format(value[0]),
                    "G : {}".format(value[1]),
                    "B : {}".format(value[2]),
                    "alpha : {}".format(value[3])
                ]
            else:
                status_list = [
                    "( x : {}, y :{} )".format(x, y),
                    "gray value : {}".format(value),
                ]

            for statbar, stat in zip(self.statbar_list, status_list):
                statbar.showMessage(stat)

    def next_frame(self):
        """Get next frame from the connected camera.

        Get next frame, set it to the view area and update.
        """
        #print("display :", self.is_display)
        if self.is_display:
            self.camera.read_frame()
            self.convert_frame()
            self.scene.clear()
            self.scene.addPixmap(self.pixmap)
            self.update()
            #print("update")

    def convert_frame(self):
        """Convert the class of frame

        Create qimage, qpixmap objects from ndarray frame for displaying on the window.

        """
        if self.colorspace == "rgb":
            self.qimage = QImage(
                self.camera.frame.data,
                self.camera.frame.shape[1],
                self.camera.frame.shape[0],
                self.camera.frame.shape[1] * 3,
                QImage.Format_RGB888
                )
        elif self.colorspace == "gray":
            self.qimage = QImage(
                self.camera.frame.data,
                self.camera.frame.shape[1],
                self.camera.frame.shape[0],
                self.camera.frame.shape[1] * 1,
                QImage.Format_Grayscale8)

        self.pixmap.convertFromImage(self.qimage)

    def save_frame(self):
        """Save the frame on the window as an image.
        """
        if self.filename_rule == "Manual":
            self.save_frame_manual()
            if not self.filename:
                return None
            prm = re.sub(r"\.(.*)", ".csv", str(self.filename))
        else:
            self.filename = FileIO.get_filename(self.filename_rule, self.image_suffix, self.parent_dir)
            prm = str(self.filename).replace(self.image_suffix, "csv")

        if not self.dst.exists():
            self.dst.mkdir(parents=True)
        im = Image.fromarray(self.camera.frame)
        im.save(self.filename)

        # make a parameter file
        with open(prm, "w") as f:
            for name, key in self.current_params.items():
                f.write("{},{}\n".format(name, self.current_params[name]["value"]))

        self.write_text("{:<10}: {}".format("save image", self.filename))
        self.write_text("{:<10}: {}".format("save param", prm))

    def update_prop_table(self):
        """Updates the table that shows the camera properties.
        """
        w, h, cc, f = self.camera.get_properties()
        self.prop_table = [
            ["Fourcc", cc],
            ["Width", int(w)],
            ["Height", int(h)],
            ["FPS", "{:.1f}".format(f)],
            ["Bit depth", 8],
            ["Naming Style", self.filename_rule]
        ]
        col = 1
        for row in range(len(self.prop_table)):
            text = str(self.prop_table[row][col])
            self.prop_table_widget.item(row, col).setText(text)

    def record(self):
        """Start or end recording
        """
        if self.camera.is_recording:
            self.camera.stop_recording()
            self.rec_button.setText('&Rec')
            self.rec_act.setText('&Record')
            self.write_text("save : {}".format(self.video_filename))
        else:
            self.video_filename = FileIO.get_filename(self.filename_rule, self.video_suffix, self.parent_dir)
            self.camera.start_recording(self.video_filename, self.video_codec)
            self.rec_button.setText('Stop rec')
            self.rec_act.setText('Stop record')

    @display
    def save_frame_manual(self) -> bool:
        """Determine file name of image to save with QFileDialog
        """
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle("Save File")
        self.dialog.setNameFilters([
            "image (*.jpg *.png *.tiff *.pgm)",
            "All Files (*)"
            ])
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.setOption(QFileDialog.DontUseNativeDialog)

        if self.dialog.exec_():
            r = self.dialog.selectedFiles()

            # If the file name doesn't include supproted suffixes, add to the end.
            if re.search(".pgm$|.png$|.jpg$|.tiff$", r[0]):
                self.filename = r[0]
            else:
                self.filename = "{}.{}".format(r[0], self.image_suffix)
            return True
        else:
            return False

    def get_screensize(self):
        """Get current screen size from the output of linux cmd `xrandr`.
        """
        cmd = ["xrandr"]
        ret = subprocess.check_output(cmd)
        output = ret.decode()
        pattern = r"current(\s+\d+\s+x\s+\d+)"

        m = re.search(pattern, output)
        if m:
            size = re.sub(" ", "", m.group(1))
            w, h = map(int, size.split("x"))
            return w, h, size
        else:
            return None

    def set_sliderval(self, param: str, value: int):
        """Changes a camera parameter.

        Updates the label on the right of the slider if input value is valid.

        Args:
            param (str): A camera parameter
            value (int): its value
        """
        val = self.camera.set_parameter(param, value)
        self.current_params[param]["value"] = str(val)
        self.current_params[param]["slider_value"].setText(str(value))

    def set_param_default(self):
        """Sets all paramters to default.
        """
        for param, values in self.current_params.items():
            default = values["default"]
            self.camera.set_parameter(param, default)
            self.current_params[param]["slider"].setValue(int(default))
            self.current_params[param]["slider_value"].setText(str(default))

    def get_properties(self) -> list:
        """Get the current camera properties.

        Returns:
            list: parameters. fourcc, width, height, fps.
        """
        tmp = []
        for row in range(4):
            tmp.append(self.prop_table[row][1])
        return tmp

    def write_text(self, text: str, level: str = "info", color: str = None):
        """Writes the message into information window.

        Args:
            text (str): A text to write.
            level (str, optional): Log lebel of the message. Defaults to "info".
            color (str, optional): Font color. Defaults to None.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        now = now[:-3]
        if color == "red":
            form = f"<font color='red'>[{level.upper():<4} {now}] {text}</font>"
        elif color == "yellow":
            form = f"<font color='yellow'>[{level.upper():<4} {now}] {text}</font>"
        else:
            form = f"[{level.upper():<4} {now}] {text}"
        self.text_edit.append(form)
