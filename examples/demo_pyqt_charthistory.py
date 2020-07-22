#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets as QtWid
import pyqtgraph as pg

from dvg_pyqt_charthistory import ChartHistory
from dvg_pyqt_controls import SS_GROUP
from dvg_qdeviceio import QDeviceIO

if 0:
    pg.setConfigOptions(useOpenGL=True)
    pg.setConfigOptions(antialias=True)
    pg.setConfigOptions(enableExperimental=True)

pg.setConfigOption("leftButtonPan", False)

# Constants
Fs = 10000  # Sampling rate of the simulated data [Hz]
WORKER_DAQ_INTERVAL_MS = 1000 / 50  # [ms]
CHART_DRAW_INTERVAL_MS = 1000 / 25  # [ms]
CHART_HISTORY_TIME = 10  # 10 [s]

# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------


class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(50, 50, 800, 660)
        self.setWindowTitle("ChartHistory demo")

        # Create PlotItem
        self.gw_chart = pg.GraphicsWindow()
        self.pi_chart = self.gw_chart.addPlot()

        p = {"color": "#CCC", "font-size": "10pt"}
        self.pi_chart.showGrid(x=1, y=1)
        self.pi_chart.setLabel("bottom", text="history (sec)", **p)
        self.pi_chart.setLabel("left", text="amplitude", **p)
        self.pi_chart.setRange(
            xRange=[-1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04],
            yRange=[-1.1, 1.1],
            disableAutoRange=True,
        )

        # Create ChartHistory and PlotDataItem and link them together
        PEN_01 = pg.mkPen(color=[0, 200, 0], width=3)
        self.CH_1 = ChartHistory(
            capacity=round(CHART_HISTORY_TIME * Fs),
            linked_curve=self.pi_chart.plot(pen=PEN_01),
        )

        # Options
        self.qpbt_option_1 = QtWid.QPushButton("Pause/unpause")
        self.qpbt_option_1.clicked.connect(self.process_qpbt_option_1)
        self.qpbt_option_2 = QtWid.QPushButton("Option 2")
        self.qpbt_option_2.clicked.connect(self.process_qpbt_option_2)
        self.qpbt_option_3 = QtWid.QPushButton("Option 3")
        self.qpbt_option_3.clicked.connect(self.process_qpbt_option_3)

        grid = QtWid.QGridLayout()
        grid.addWidget(self.qpbt_option_1, 0, 0)
        grid.addWidget(self.qpbt_option_2, 1, 0)
        grid.addWidget(self.qpbt_option_3, 2, 0)
        grid.setAlignment(QtCore.Qt.AlignTop)

        qgrp_options = QtWid.QGroupBox("")
        qgrp_options.setStyleSheet(SS_GROUP)
        qgrp_options.setLayout(grid)

        # 'Chart'
        self.qpbt_clear_chart = QtWid.QPushButton("Clear")
        self.qpbt_clear_chart.clicked.connect(self.process_qpbt_clear_chart)

        grid = QtWid.QGridLayout()
        grid.addWidget(self.qpbt_clear_chart, 0, 0)
        grid.setAlignment(QtCore.Qt.AlignTop)

        qgrp_chart = QtWid.QGroupBox("Chart")
        qgrp_chart.setStyleSheet(SS_GROUP)
        qgrp_chart.setLayout(grid)

        vbox = QtWid.QVBoxLayout()
        vbox.addWidget(qgrp_options)
        vbox.addWidget(qgrp_chart)
        vbox.addStretch()

        # Round up bottom frame
        hbox_bot = QtWid.QHBoxLayout()
        hbox_bot.addWidget(self.gw_chart, 1)
        hbox_bot.addLayout(vbox, 0)

        # -------------------------
        #   Round up full window
        # -------------------------

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox_bot, stretch=1)

    # --------------------------------------------------------------------------
    #   Handle controls
    # --------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def process_qpbt_clear_chart(self):
        str_msg = "Are you sure you want to clear the chart?"
        reply = QtWid.QMessageBox.warning(
            window,
            "Clear chart",
            str_msg,
            QtWid.QMessageBox.Yes | QtWid.QMessageBox.No,
            QtWid.QMessageBox.No,
        )

        if reply == QtWid.QMessageBox.Yes:
            self.CH_1.clear()

    @QtCore.pyqtSlot()
    def process_qpbt_option_1(self):
        if timer_chart.isActive():
            timer_chart.stop()
        else:
            timer_chart.start()

    @QtCore.pyqtSlot()
    def process_qpbt_option_2(self):
        print("option 2")

    @QtCore.pyqtSlot()
    def process_qpbt_option_3(self):
        print("option 3")


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


@QtCore.pyqtSlot()
def about_to_quit():
    qdev.quit()
    timer_chart.stop()


def DAQ_function():
    x = np.arange(WORKER_DAQ_INTERVAL_MS * Fs / 1e3) / Fs + time.perf_counter()
    y = np.sin(2 * np.pi * 100 * x)
    window.CH_1.add_new_readings(x, y)

    return True


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    app.aboutToQuit.connect(about_to_quit)

    window = MainWindow()

    class FakeDevice:
        def __init__(self):
            self.name = "FakeDevice"
            self.is_alive = True

    # Fake a device that generates data at a sampling rate of `Fs` Hz. The
    # data gets generated and transferred to our ChartHistory-instance from
    # out of a separate thread. This is taken care of by QDeviceIO.
    qdev = QDeviceIO(dev=FakeDevice())
    qdev.create_worker_DAQ(
        DAQ_interval_ms=WORKER_DAQ_INTERVAL_MS, DAQ_function=DAQ_function
    )
    qdev.start()

    # Chart refresh rate
    timer_chart = QtCore.QTimer(timerType=QtCore.Qt.PreciseTimer)
    timer_chart.timeout.connect(window.CH_1.update_curve)
    timer_chart.start(CHART_DRAW_INTERVAL_MS)

    window.show()
    sys.exit(app.exec_())
