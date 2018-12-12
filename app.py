import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QMainWindow,
                             QShortcut, QWidget)

from gearset import GearSet
from gearsetwidget import GearSetWidget

class ChaosTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self._gear_set_1 = GearSet()
        self._gear_set_2 = GearSet()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Create a new widget for central widget to apply grid layout
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Set vbox layout to central widget
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        widget_central.setLayout(vbox)
        self.widget_gear_set_1 = GearSetWidget(self._gear_set_1)
        self.widget_gear_set_2 = GearSetWidget(self._gear_set_2)
        vbox.addWidget(self.widget_gear_set_1)
        vbox.addWidget(self.widget_gear_set_2)

        self.shortcut_exit = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_exit.activated.connect(self.close)

        self.setGeometry(685, 990, 300, 10)

        self.show()

if __name__ == "__main__":
    new_font = QFont("Consolas", 8)
    app = QApplication(sys.argv)
    chaos_tracker_app = ChaosTrackerApp()
    app.setFont(new_font)
    sys.exit(app.exec_())
