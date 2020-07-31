#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets as QtWid
import pyqtgraph as pg

import dvg_pyqt_controls as controls


# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------


class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(350, 50, 800, 660)
        self.setWindowTitle("Demo: dvg_pyqt_controls")

        def grid_add(
            grid: QtWid.QGridLayout, label: str, control: QtWid.QWidget
        ):
            row_idx = grid.rowCount()
            grid.addWidget(QtWid.QLabel(label), row_idx, 0)
            grid.addWidget(control, row_idx, 1)

        def grid_add_double(
            grid: QtWid.QGridLayout,
            label: str,
            control_1: QtWid.QWidget,
            control_2: QtWid.QWidget,
        ):
            row_idx = grid.rowCount()
            grid.addWidget(QtWid.QLabel(label), row_idx, 0)
            grid.addWidget(control_1, row_idx, 1)
            grid.addWidget(control_2, row_idx, 2)

        grid = QtWid.QGridLayout()
        grid.addWidget(QtWid.QLabel("LED's"), 0, 0)
        grid.setRowMinimumHeight(grid.rowCount(), 20)

        led_1a = controls.create_LED_indicator()
        led_1b = controls.create_LED_indicator()
        led_2a = controls.create_LED_indicator_rect()
        led_2b = controls.create_LED_indicator_rect()
        led_3a = controls.create_tiny_error_LED()
        led_3b = controls.create_tiny_error_LED()
        led_4a = controls.create_tiny_LED()
        led_4b = controls.create_tiny_LED()
        led_5a = controls.create_error_LED()
        led_5b = controls.create_error_LED()

        grid_add_double(grid, "LED indicator", led_1a, led_1b)
        grid_add_double(grid, "LED indicator rect", led_2a, led_2b)
        grid_add_double(grid, "Tiny error LED", led_3a, led_3b)
        grid_add_double(grid, "Tiny LED", led_4a, led_4b)
        grid_add_double(grid, "Error LED", led_5a, led_5b)

        grid.setRowMinimumHeight(grid.rowCount(), 20)
        grid.addWidget(QtWid.QLabel("Buttons"), grid.rowCount(), 0)
        grid.setRowMinimumHeight(grid.rowCount(), 20)

        btn_1 = controls.create_Relay_button()
        btn_2 = controls.create_Toggle_button()
        btn_3 = controls.create_Toggle_button_2()
        btn_4 = controls.create_Toggle_button_3()

        grid_add(grid, "Relay button", btn_1)
        grid_add(grid, "Toggle button", btn_2)
        grid_add(grid, "Toggle button 2", btn_3)
        grid_add(grid, "Toggle button 3", btn_4)

        # 'LegendBox'
        PEN_1 = pg.mkPen(color=[255, 30, 180], width=3)
        PEN_2 = pg.mkPen(color=[0, 255, 255], width=3)
        PEN_3 = pg.mkPen(color=[255, 255, 90], width=3)

        self.legend_box = controls.LegendBox(
            text=["wave 1", "wave 2", "Lissajous"],
            pen=[PEN_1, PEN_2, PEN_3],
            checked=[True, True, True],
        )

        vbox = QtWid.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch()

        # Round up frame
        hbox = QtWid.QHBoxLayout()
        hbox.addLayout(vbox, 0)
        hbox.addStretch()

        # -------------------------
        #   Round up full window
        # -------------------------

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox, stretch=1)


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
