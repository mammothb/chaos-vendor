from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout, QListWidget, QWidget

class TrackGearWidget(QWidget):
    signal_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self._list = QListWidget(self)
        self._list.setMinimumSize(QSize(50, 100))
        grid.addWidget(self._list, 0, 0)

    @pyqtSlot(object)
    def compute_desired_gear(self, current_gear_amount):
        self._list.clear()
        for i, (key, value) in enumerate(current_gear_amount.items()):
            self._list.addItem(key)
            if value == 0:
                self._list.item(i).setForeground(QColor("red"))
            if value == 1:
                self._list.item(i).setForeground(QColor("orange"))
