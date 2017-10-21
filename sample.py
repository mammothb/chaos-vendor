from PyQt5 import QtCore, QtGui, QtWidgets


class widgetB(QtWidgets.QWidget):

    procDone = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetB, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.button = QtWidgets.QPushButton("Send Message to A", self)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        self.procDone.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_procStart(self, message):
        print(message)
        # self.lineEdit.setText("From A: " + message)

        # self.raise_()


class widgetA(QtWidgets.QWidget):
    procStart = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(widgetA, self).__init__(parent)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setText("Hello!")

        self.button = QtWidgets.QPushButton("Send Message to B", self)
        self.button.clicked.connect(self.on_button_clicked)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)


    def on_button_clicked(self):
        print("clicked A")
        self.send_signal()

    @QtCore.pyqtSlot()
    def send_signal(self):
        self.procStart.emit(self.lineEdit.text())

    @QtCore.pyqtSlot(str)
    def on_widgetB_procDone(self, message):
        # print(message)
        print("A")
        # self.lineEdit.setText("From B: " + message)

        # self.raise_()


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        widget_central = QtWidgets.QWidget()

        self.setCentralWidget(widget_central)
        grid = QtWidgets.QGridLayout()
        widget_central.setLayout(grid)

        self.widgetA = widgetA()
        self.widgetB = widgetB()

        grid.addWidget(self.widgetA, 0, 0)
        grid.addWidget(self.widgetB, 0, 1)

        self.widgetA.procStart.connect(self.widgetB.on_procStart)
        self.widgetB.procDone.connect(self.widgetA.on_widgetB_procDone)

        # self.widgetB.show()
        self.widgetA.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = mainwindow()
    main.show()
    sys.exit(app.exec_())
