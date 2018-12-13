import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QShortcut, QVBoxLayout,
                             QWidget)

from gearset import GearSet
from gearsetwidget import GearSetWidget
from trackgearsetwidget import TrackGearSetWidget

class ChaosTrackerApp(QMainWindow):
    def __init__(self, win_id):
        super().__init__()
        self._win_id = win_id
        self._gear_set_1 = GearSet()
        self._gear_set_2 = GearSet()
        self.init_ui()
        self.set_style_sheet()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Create a new widget for central widget to apply grid layout
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Set vbox layout to central widget
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.widget_gear_set_1 = GearSetWidget(self._gear_set_1)
        self.widget_gear_set_2 = GearSetWidget(self._gear_set_2)
        vbox.addWidget(self.widget_gear_set_1)
        vbox.addWidget(self.widget_gear_set_2)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        x = 700
        y = 990
        label_x = QLabel("x:")
        label_y = QLabel("y:")
        self.edit_x = QLineEdit(str(x))
        self.edit_y = QLineEdit(str(y))

        label_x.setFixedWidth(20)
        label_y.setFixedWidth(20)
        self.edit_x.setFixedWidth(40)
        self.edit_y.setFixedWidth(40)

        button = QPushButton("Move")
        button.setObjectName("moveButton")
        button.setFixedWidth(40)
        button.clicked.connect(self.move_window)
        self.widget_track_gear_set = TrackGearSetWidget(
            self._win_id, self.widget_gear_set_1, self.widget_gear_set_2)

        hbox.addWidget(label_x)
        hbox.addWidget(self.edit_x)
        hbox.addWidget(label_y)
        hbox.addWidget(self.edit_y)
        hbox.addWidget(button)
        hbox.addWidget(self.widget_track_gear_set)

        vbox.addLayout(hbox)
        widget_central.setLayout(vbox)

        self.shortcut_exit = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_exit.activated.connect(self.close)

        self.setGeometry(x, y, 300, 10)

        self.show()

    def move_window(self):
        x = try_parse_int64(self.edit_x.text())
        y = try_parse_int64(self.edit_y.text())
        if x is not None and y is not None:
            self.move(x, y)

    def set_style_sheet(self):
        self.setStyleSheet("""
            QPushButton#moveButton {
                background-color: #819033;
                border-style: outset;
                border-width: 1px;
                border-color: #F8E9A8;
                color: black;
                font: 12px;
                padding: 1px;
            }
            QLineEdit {
                background-color: #F8E9A8;
                border-style: outset;
                border-width: 1px;
                border-color: #F8E9A8;
                color: black;
                font: 12px;
                padding: 1px;
            }
        """)

def try_parse_int64(string):
    try:
        ret = int(string)
    except ValueError:
        return None
    return None if ret < -2 ** 64 or ret >= 2 ** 64 else ret

if __name__ == "__main__":
    new_font = QFont("Consolas")
    app = QApplication(sys.argv)
    app.setFont(new_font)
    long_qdesktop_id = QApplication.desktop().winId()
    chaos_tracker_app = ChaosTrackerApp(long_qdesktop_id)
    sys.exit(app.exec_())
