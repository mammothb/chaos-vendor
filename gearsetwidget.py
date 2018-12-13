from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget

class GearSetWidget(QWidget):
    def __init__(self, gear_set):
        super().__init__()
        self._gear_set = gear_set
        self._buttons = {}
        self.init_ui(gear_set)
        self.set_style_sheet()

    def init_ui(self, gear_set):
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)
        gear_set_status = gear_set.get_gear_set()
        for i, (key, value) in enumerate(gear_set_status.items()):
            button = QPushButton(key)
            button.setObjectName("gearButton")
            button.setCheckable(True)
            button.setChecked(value)
            button.setEnabled(False)
            button.clicked[bool].connect(self.update_gear_status)
            self._buttons[key] = button
            grid.addWidget(button, 0, i)

    def set_style_sheet(self):
        self.setStyleSheet("""
            QPushButton#gearButton:disabled {
                background-color: #F8E9A8;
                border-style: outset;
                border-width: 1px;
                border-color: #F8E9A8;
                color: black;
                font: 12px;
                min-width: 2.8em;
                padding: 1px;
            }
            QPushButton#gearButton:disabled:checked {
                background-color: #BC3C4B;
                border-style: inset;
            }
        """)

    def set_button_checked(self, key, pressed):
        self._buttons[key].setChecked(pressed)
        self._gear_set.set_gear(key, pressed)

    def update_gear_status(self, pressed):
        source = self.sender()
        self._gear_set.set_gear(source.text(), pressed)

    def reset_gear_status(self):
        self._gear_set.reset_gear_set()
        for button in self._buttons:
            button.setChecked(False)
