import re
from pathlib import Path
import sys

from PIL import Image
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, \
    QAbstractScrollArea, QStatusBar, QGridLayout, QAbstractItemView, \
    QTableWidgetItem, QSizePolicy, QFileDialog

from EvisionCamera.camera import LinuxCamera, WindowsCamera
from EvisionCamera.fileIO import FileIO
from EvisionCamera.slot import Slot
from EvisionCamera.EvisionCamera_ui import Ui_EvisionCameraForm
from EvisionCamera.util import Utility
import numpy as np


class EvisionCamera(QWidget):
    def __init__(self):
        super(EvisionCamera, self).__init__()
        self.ui = Ui_EvisionCameraForm()
        self.ui.setupUi(self)
        self.device = 0
        self.camtype = "usb_cam"
        self.colorspace = "rgb"
        self.image_suffix = "png"
        self.video_codec = "AVC1"
        self.video_suffix = "avi"
        self.dst = Path("./")
        self.parent_dir = Path(__file__).parent.resolve()

        self.filename_rule_lst = FileIO.file_save
        self.filename_rule = FileIO.file_save_lst[-1]

        self.is_display = True
        self.param_separate = False

        self.slot = Slot(self)

        cam = self.get_cam()

        self.camera = cam(self.device, self.colorspace, parent=self)
        self.support_params = self.camera.get_supported_params()
        self.current_params = self.camera.get_current_params("full")

        self.prop_table = [["Fourcc", "aa"],
                           ["Width", 640],
                           ["Height", 480],
                           ["FPS", 30.0],
                           ["Bit depth", 8],
                           ["File naming style", self.filename_rule]]

        self.setup()
        self.set_timer()

    def get_cam(self):
        """Return camera object according to current OS.

        Detects what OS you are using, return camera objects  in order to function properly.

            - Linux: LinuxCamera
            - RaspberryPi OS: RaspiCamera
            - Windows: WindowsCamera

        Returns:
            Camera class
        """
        self.system = sys.platform
        if self.system == 'linux':
            return LinuxCamera
        elif self.system == 'win32':
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
        # self.information_window_setup()
        self.view_setup()
        self.layout_setup()
        self.image_setup()
        self.update_prop_table()
        self.adjust_windowsize()

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
        if self.colorspace == "rgb" or self.colorspace == "RGB":
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

    def view_setup(self):
        """Set view area to diplay read frame in part of the main window
        """
        self.scene = QGraphicsScene()
        self.ui.view.setScene(self.scene)
        self.width = 640
        self.height = 480
        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.ui.view.setMouseTracking(True)
        self.ui.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ui.view.setCacheMode(QGraphicsView.CacheBackground)
        self.ui.view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

    def layout_setup(self):
        """Set layout of objects on the window.
        """
        # self.add_statusbar()
        self.add_buttons()
        self.add_prop_window()

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
                # self.ssetStatusBar(stat)
                self.statbar_list[0].reformat()
                first = False
            else:
                self.statbar_list[0].addPermanentWidget(stat)

    def add_buttons(self):
        self.ui.save_button.clicked.connect(self.save_frame)
        self.ui.stop_button.clicked.connect(self.stop_frame)
        self.ui.rec_button.clicked.connect(self.record)
        self.ui.close_button.clicked.connect(self.slot.quit)
        self.ui.theme_button.clicked.connect(self.slot.switch_theme)
        self.ui.help_button.clicked.connect(self.slot.usage)
        self.ui.frame_button.clicked.connect(self.slot.change_frame_prop)
        self.ui.default_button.clicked.connect(self.set_param_default)
        self.ui.filerule_button.clicked.connect(self.slot.set_file_rule)
        pass

    def add_prop_window(self):
        """Create a table to show the current properties of camera.

        Returns:
            QGridLayout: PySide2 QGridLayout
        """
        header = ["property", "value"]

        self.ui.prop_table_widget.setColumnCount(len(header))
        self.ui.prop_table_widget.setRowCount(len(self.prop_table))

        self.ui.prop_table_widget.setHorizontalHeaderLabels(header)
        self.ui.prop_table_widget.verticalHeader().setVisible(False)
        self.ui.prop_table_widget.setAlternatingRowColors(True)
        self.ui.prop_table_widget.horizontalHeader().setStretchLastSection(True)
        self.ui.prop_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.prop_table_widget.setFocusPolicy(Qt.NoFocus)

        for row, content in enumerate(self.prop_table):
            for col, elem in enumerate(content):
                self.item = QTableWidgetItem(elem)
                self.ui.prop_table_widget.setItem(row, col, self.item)
        self.ui.prop_table_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # self.prop_table_widget.resizeColumnsToContents()
        # self.prop_table_widget.resizeRowsToContents()
        self.ui.prop_table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.prop_table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.prop_table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.ui.prop_table_widget.setColumnWidth(0, 150)
        self.ui.prop_table_widget.setColumnWidth(1, 150)

    # slot save_button_down
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

    def stop_frame(self, checked: bool):
        """Stop reading next frame.

        Args:
            checked (bool): True when presse the Stop button (toggle on). False when press
                again (toggel off).
        """
        if checked:
            self.write_text("Stop !!")
            self.is_display = False
            self.ui.stop_button.setText('Start')
            self.ui.stop_button.setChecked(True)
        else:
            self.write_text("Start !!")
            self.is_display = True
            self.ui.stop_button.setText('&Pause')
            self.ui.stop_button.setChecked(False)

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
            self.ui.prop_table_widget.item(row, col).setText(text)

    def adjust_windowsize(self):
        """Adjusts the main window size
        """
        system = Utility.get_os()
        # if system == "linux":
        #     w, h, _ = self.get_screensize()
        #     wscale = 0.5
        #     hscale = 0.7
        #     self.resize(wscale * w, hscale * h)
        # else:
        self.resize(800, 600)

    def set_param_default(self):
        """Sets all paramters to default.
        """
        for param, values in self.current_params.items():
            default = values["default"]
            self.camera.set_parameter(param, default)
            self.current_params[param]["slider"].setValue(int(default))
            self.current_params[param]["slider_value"].setText(str(default))

    def write_text(self, text: str, level: str = "info", color: str = None):
        print(text)

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

    def get_properties(self) -> list:
        """Get the current camera properties.

        Returns:
            list: parameters. fourcc, width, height, fps.
        """
        tmp = []
        for row in range(4):
            tmp.append(self.prop_table[row][1])
        return tmp