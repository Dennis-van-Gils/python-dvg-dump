#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List

from PyQt5 import QtCore
from PyQt5 import QtWidgets as QtWid

import dvg_pyqt_controls as c


# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------


class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(350, 50, 800, 660)
        self.setWindowTitle("Demo: dvg_pyqt_controls")

        def add2grid(
            grid: QtWid.QGridLayout,
            labels: List[QtWid.QWidget],
            controls: List[QtWid.QWidget],
        ):
            for idx, control in enumerate(controls):
                row_idx = grid.rowCount()
                grid.addWidget(labels[idx], row_idx, 0)
                grid.addWidget(control, row_idx, 1)

        def add2box(hbox, N, create_control_fun):
            controls = list()
            labels = list()
            for i in range(N):
                controls.append(create_control_fun())
                labels.append(QtWid.QLabel("%d" % i))

            grid = QtWid.QGridLayout()
            add2grid(grid, labels, controls)
            grid.setAlignment(QtCore.Qt.AlignTop)

            descr = create_control_fun.__name__
            descr = descr.replace("create_", "")
            descr = descr.replace("_", " ")
            grpb = QtWid.QGroupBox(descr)
            grpb.setStyleSheet(c.SS_GROUP)
            grpb.setLayout(grid)

            hbox.addWidget(grpb, stretch=0, alignment=QtCore.Qt.AlignTop)
            return (controls, labels)

        # ----------------------------------------------------------------------
        #   LEDs
        # ----------------------------------------------------------------------

        hbox_1 = QtWid.QHBoxLayout()
        leds_1, lbls_1 = add2box(hbox_1, 8, c.create_LED_indicator)
        leds_2, lbls_2 = add2box(hbox_1, 4, c.create_LED_indicator_rect)
        leds_3, lbls_3 = add2box(hbox_1, 4, c.create_error_LED)
        leds_4, lbls_4 = add2box(hbox_1, 4, c.create_tiny_LED)
        leds_5, lbls_5 = add2box(hbox_1, 4, c.create_tiny_error_LED)

        uber_leds = [leds_1, leds_2, leds_3, leds_4, leds_5]
        uber_lbls = [lbls_1, lbls_2, lbls_3, lbls_4, lbls_5]

        for i, leds in enumerate(uber_leds):
            for j, led in enumerate(leds):
                if j < 2:
                    checked = False
                    enabled = False
                    control_text = "0" if i < 3 else ""
                    label_text = "Disabled & False"
                elif j < 4:
                    checked = True
                    enabled = False
                    control_text = "1" if i < 3 else ""
                    label_text = "Disabled & True"
                elif j < 6:
                    checked = False
                    enabled = True
                    control_text = "0" if i < 3 else ""
                    label_text = "Enabled & False"
                else:
                    checked = True
                    enabled = True
                    control_text = "1" if i < 3 else ""
                    label_text = "Enabled & True"

                led.setChecked(checked)
                led.setEnabled(enabled)
                led.setText(control_text)
                uber_lbls[i][j].setText(label_text)

        # ----------------------------------------------------------------------
        #   Buttons
        # ----------------------------------------------------------------------

        hbox_2 = QtWid.QHBoxLayout()
        btns_1, lbls_1 = add2box(hbox_2, 8, c.create_Relay_button)
        btns_2, lbls_2 = add2box(hbox_2, 8, c.create_Toggle_button)
        btns_3, lbls_3 = add2box(hbox_2, 8, c.create_Toggle_button_2)
        btns_4, lbls_4 = add2box(hbox_2, 8, c.create_Toggle_button_3)

        uber_btns = [btns_1, btns_2, btns_3, btns_4]
        uber_lbls = [lbls_1, lbls_2, lbls_3, lbls_4]

        for i, btns in enumerate(uber_btns):
            for j, btn in enumerate(btns):
                if j < 2:
                    checked = False
                    enabled = False
                    label_text = "Disabled & False"
                elif j < 4:
                    checked = True
                    enabled = False
                    label_text = "Disabled & True"
                elif j < 6:
                    checked = False
                    enabled = True
                    label_text = "Enabled & False"
                else:
                    checked = True
                    enabled = True
                    label_text = "Enabled & True"

                btn.setChecked(checked)
                btn.setEnabled(enabled)
                btn.setText(control_text)
                uber_lbls[i][j].setText(label_text)

        for btn in btns_1:
            btn.setText("0" if not btn.isChecked() else "1")
        for btn in btns_2:
            btn.setText("False" if not btn.isChecked() else "True")
        for btn in btns_3:
            btn.setText("Off Okay" if not btn.isChecked() else "ON !!")
        for btn in btns_4:
            btn.setText("OFF !!" if not btn.isChecked() else "On Okay")

        # -------------------------
        #   Round up full window
        # -------------------------

        hbox_1.addStretch()
        hbox_2.addStretch()

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox_1, stretch=0)
        vbox.addLayout(hbox_2, stretch=0)
        vbox.addStretch()


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
