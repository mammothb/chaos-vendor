import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QAction, QApplication, QGridLayout, QMainWindow,
                             QWidget)

import gearset
import gearsetwidget
import trackgearwidget

class ChaosVendorApp(QMainWindow):
    signal_compute = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self._gear_set_1 = gearset.GearSet()
        self._gear_set_2 = gearset.GearSet()
        self.load_gear_set()
        self.init_ui()

    def load_gear_set(self):
        pass

    def init_ui(self):
        # Create a new widget for central widget to apply grid layout
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        # Set grid layout to central widget
        grid = QGridLayout()
        widget_central.setLayout(grid)
        self.widget_gear_set_1 = gearsetwidget.GearSetWidget(
            self._gear_set_1)
        self.widget_gear_set_2 = gearsetwidget.GearSetWidget(
            self._gear_set_2)
        self.widget_track_gear = trackgearwidget.TrackGearWidget()
        grid.addWidget(self.widget_gear_set_1, 0, 0)
        grid.addWidget(self.widget_gear_set_2, 0, 1)
        grid.addWidget(self.widget_track_gear, 0, 2)

        self.widget_gear_set_1.signal_updated.connect(self.update_values)
        self.widget_gear_set_2.signal_updated.connect(self.update_values)
        self.signal_compute.connect(
            self.widget_track_gear.compute_desired_gear)

        action_exit = QAction("Exit", self)
        action_exit.setShortcut("Ctrl+W")
        action_exit.setStatusTip("Exit application")
        action_exit.triggered.connect(self.close)

        # Status bar at the bottom
        self.statusBar()

        # Menu bar at the top
        menu_bar = self.menuBar()
        menu_file = menu_bar.addMenu("&File")
        menu_file.addAction(action_exit)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("Chaos Vendor")

        self.show()

    @pyqtSlot()
    def update_values(self):
        """Receives signal from GearSetWidget and calculates current amount
        of gear
        """
        current_gear_amount = {}
        for (key, value_1), (__, value_2) in zip(
                self._gear_set_1.get_gear_set().items(),
                self._gear_set_2.get_gear_set().items()):
            # cast to int
            current_gear_amount[key] = int(value_1) + int(value_2)
        self.signal_compute.emit(current_gear_amount)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chaos_vendor_app = ChaosVendorApp()
    sys.exit(app.exec_())
