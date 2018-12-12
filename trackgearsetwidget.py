import os.path

import cv2
import numpy as np
from pynput import mouse
from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget

class TrackGearSetWidget(QWidget):
    def __init__(self, win_id, gear_set_1, gear_set_2):
        super().__init__()
        self._win_id = win_id
        self._screen = QApplication.primaryScreen()
        self._box = [0] * 4
        cwd = os.path.realpath(os.path.dirname(__file__))
        self._filename = os.path.join(cwd, "stash_area.png")
        self._processed_filename = os.path.join(cwd, "final_img.png")
        self._coords = []
        self._side_length = None
        self._gear_set = [gear_set_1, gear_set_2]
        self._gear_grid = [
            {
                "belt": [32, 33],
                "boot": [28, 29, 34, 35],
                "chest": [14, 15, 20, 21, 26, 27],
                "glove": [24, 25, 30, 31],
                "helm": [2, 3, 8, 9],
                "neck": [4],
                "ring1": [10],
                "ring2": [11],
                "weap": [0, 1, 6, 7, 12, 13, 18, 19]
            },
            {
                "belt": [68, 69],
                "boot": [64, 65, 70, 71],
                "chest": [50, 51, 56, 57, 62, 63],
                "glove": [60, 61, 66, 67],
                "helm": [38, 39, 44, 45],
                "neck": [40],
                "ring1": [46],
                "ring2": [47],
                "weap": [36, 37, 42, 43, 48, 49, 54, 55]
            }
        ]

        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)
        button = QPushButton("Setup")
        button.setObjectName("trackButton")
        button.clicked[bool].connect(self.setup_stash_grid)
        grid.addWidget(button, 0, 0)

        button = QPushButton("Update")
        button.setObjectName("trackButton")
        button.clicked[bool].connect(self.track_gear_status)
        grid.addWidget(button, 0, 1)

        self.setStyleSheet("""
            QPushButton#trackButton {
                background-color: #819033;
                border-style: outset;
                border-width: 1px;
                border-color: #F8E9A8;
                font: 12px;
                min-width: 3em;
                padding: 1px;
            }
        """)

    def setup_stash_grid(self):
        self._get_box()
        self._capture_stash()
        self._get_grid()

    def track_gear_status(self):
        self._capture_stash()
        img = cv2.imread(self._filename, 0)
        __, img_bin = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
        cv2.imwrite("img_bin.png", img_bin)
        for n, gear_dict in enumerate(self._gear_grid):
            for k in gear_dict:
                val = []
                for idx in gear_dict[k]:
                    i, j = self._coords[idx][1], self._coords[idx][0]
                    val.append(np.mean(img_bin[i : i + self._side_length,
                                               j : j + self._side_length]))
                self._gear_set[n].set_button_checked(k, np.mean(val) > 10.0)

    def _get_box(self):
        """Return the top left and bottom right coordinates of a screen
        selection
        """
        def on_click(x, y, __, pressed):
            if pressed:
                self._box[0], self._box[1] = x, y
            else:
                self._box[2], self._box[3] = x, y
                return False
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def _capture_stash(self):
        x0 = self._box[0]
        y0 = self._box[1]
        width = self._box[2] - self._box[0]
        height = self._box[3] - self._box[1]
        capture = self._screen.grabWindow(self._win_id, x0, y0, width,
                                          height).toImage()
        cwd = os.path.realpath(os.path.dirname(__file__))
        self._filename = os.path.join(cwd, "stash_area.png")
        capture.save(self._filename)

    def _get_grid(self):
        img = cv2.imread(self._filename, 0)
        __, img_bin = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)

        # Defining a kernel length
        kern_len = np.array(img).shape[1] // 20
        # A verticle kernel of (1 X kernel_length) to detect vertical line
        vert_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kern_len))
        # A horizontal kernel of (kernel_length X 1) to detect horizontal line
        hori_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (kern_len, 1))
        # A kernel of (3 X 3) ones.
        kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Morphological operation to detect vertical lines from an image
        tmp_img_1 = cv2.erode(img_bin, vert_kern, iterations=3)
        vline_img = cv2.dilate(tmp_img_1, vert_kern, iterations=3)
        # Morphological operation to detect horizontal lines from an image
        tmp_img_2 = cv2.erode(img_bin, hori_kern, iterations=3)
        hline_img = cv2.dilate(tmp_img_2, hori_kern, iterations=3)

        # Weighting parameters to decide the contribution of each image
        w1 = 0.5
        # Adds two images to get a third image
        grid_img = cv2.addWeighted(vline_img, w1, hline_img, 1.0 - w1, 0.0)
        grid_img = cv2.erode(~grid_img, kern, iterations=2)
        __, grid_img = cv2.threshold(grid_img, 128, 255,
                                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        final_img, contours, __ = cv2.findContours(grid_img, cv2.RETR_LIST,
                                                   cv2.CHAIN_APPROX_SIMPLE)
        sides = []
        for cnt in contours:
            poly = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(poly) == 4:
                length = np.array([
                    abs(poly[i][0][i % 2] - poly[(i + 3) % 4][0][i % 2])
                    for i in range(4) if len(poly) == 4])
                if all(np.abs(length - np.mean(length)) < 2):
                    sides.append(np.floor(np.mean(length)))
        self._side_length = np.bincount(sides).argmax()
        for cnt in contours:
            poly = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(poly) == 4:
                length = np.array([
                    abs(poly[i][0][i % 2] - poly[(i + 3) % 4][0][i % 2])
                    for i in range(4) if len(poly) == 4])
                if all(np.abs(length - self._side_length) < 2):
                    self._coords.append(poly[0][0])
        ncol = 6
        tmp = sorted(self._coords, key=lambda k: k[1])
        for i in range(len(self._coords) // ncol):
            self._coords[i * ncol : (i + 1) * ncol] = sorted(
                tmp[i * ncol : (i + 1) * ncol], key=lambda k: k[0])
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # i = 0
        # for gear_dict in self._gear_grid:
        #     for k in gear_dict:
        #         print(i, k)
        #         for idx in gear_dict[k]:
        #             cv2.putText(final_img, k, (self._coords[idx][0],
        #                                        self._coords[idx][1] + 20),
        #                         font, 0.3, (0, 255, 0), 1, cv2.LINE_AA)
        #     i += 1
        # for i, coord in enumerate(self._coords):
        #     cv2.putText(final_img, str(i), (coord[0] + 10, coord[1] + 20),
        #                 font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        # cv2.imwrite(self._processed_filename, final_img)
