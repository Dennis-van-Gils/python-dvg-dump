#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets as QtWid
import pyqtgraph as pg

from dvg_qdeviceio import QDeviceIO
from dvg_pyqt_controls import Legend_box, SS_GROUP
from dvg_pyqtgraph_threadsafe import (
    HistoryChartCurve,
    BufferedPlotCurve,
    PlotCurve,
)

USE_OPENGL = False
if USE_OPENGL:
    print("OpenGL acceleration: Enabled")
    pg.setConfigOptions(useOpenGL=True)
    pg.setConfigOptions(antialias=True)
    pg.setConfigOptions(enableExperimental=True)

pg.setConfigOption("leftButtonPan", False)

# Constants
Fs = 1000  # Sampling rate of the simulated data [Hz]
WORKER_DAQ_INTERVAL_MS = round(1000 / 100)  # [ms]
CHART_DRAW_INTERVAL_MS = round(1000 / 50)  # [ms]
CHART_HISTORY_TIME = 10  # 10 [s]

# ------------------------------------------------------------------------------
#   MainWindow
# ------------------------------------------------------------------------------


class MainWindow(QtWid.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setGeometry(350, 50, 800, 660)
        self.setWindowTitle("ChartHistory demo")

        # Keep track of the obtained chart refresh rate
        self.obtained_chart_rate_Hz = np.nan
        self.qet_chart = QtCore.QElapsedTimer()
        self.chart_rate_accumulator = 0

        # Pause/unpause charts
        self.paused = False

        # GraphicsWindow
        capacity = round(CHART_HISTORY_TIME * Fs)
        PEN_01 = pg.mkPen(color=[0, 255, 255], width=3)
        PEN_02 = pg.mkPen(color=[255, 0, 255], width=3)
        PEN_03 = pg.mkPen(color=[0, 255, 0], width=3)
        PEN_04 = pg.mkPen(color=[255, 0, 0], width=3)

        self.gw = pg.GraphicsWindow()

        p = {"color": "#CCC", "font-size": "10pt"}
        self.plot_1 = self.gw.addPlot()
        self.plot_1.showGrid(x=1, y=1)
        self.plot_1.setTitle("title")
        self.plot_1.setLabel("bottom", text="history (sec)", **p)
        self.plot_1.setLabel("left", text="amplitude", **p)
        self.plot_1.setRange(
            xRange=[-1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04],
            yRange=[-1.1, 1.1],
            disableAutoRange=True,
        )

        self.plot_2 = self.gw.addPlot()
        self.plot_2.showGrid(x=1, y=1)
        self.plot_2.setTitle("title")
        self.plot_2.setLabel("bottom", text="history (sec)", **p)
        self.plot_2.setLabel("left", text="amplitude", **p)
        self.plot_2.setRange(
            xRange=[-1.04 * CHART_HISTORY_TIME, CHART_HISTORY_TIME * 0.04],
            yRange=[-1.1, 1.1],
            disableAutoRange=True,
        )

        self.tscurve_1 = HistoryChartCurve(
            capacity=capacity, linked_curve=self.plot_1.plot(pen=PEN_01),
        )
        self.tscurve_2 = HistoryChartCurve(
            capacity=capacity, linked_curve=self.plot_1.plot(pen=PEN_02),
        )
        self.tscurve_3 = HistoryChartCurve(
            capacity=capacity, linked_curve=self.plot_2.plot(pen=PEN_03),
        )
        self.tscurve_4 = HistoryChartCurve(
            capacity=capacity, linked_curve=self.plot_2.plot(pen=PEN_04),
        )

        self.tscurves = [
            self.tscurve_1,
            self.tscurve_2,
            self.tscurve_3,
            self.tscurve_4,
        ]

        # `Obtained rates`
        self.qlbl_DAQ_rate = QtWid.QLabel("")
        self.qlbl_DAQ_rate.setAlignment(QtCore.Qt.AlignRight)
        self.qlbl_DAQ_rate.setMinimumWidth(50)
        self.qlbl_chart_rate = QtWid.QLabel("")
        self.qlbl_chart_rate.setAlignment(QtCore.Qt.AlignRight)

        grid_rates = QtWid.QGridLayout()
        grid_rates.addWidget(QtWid.QLabel("DAQ:"), 0, 0)
        grid_rates.addWidget(QtWid.QLabel("chart:"), 1, 0)
        grid_rates.addWidget(self.qlbl_DAQ_rate, 0, 1)
        grid_rates.addWidget(self.qlbl_chart_rate, 1, 1)
        grid_rates.addWidget(QtWid.QLabel("Hz"), 0, 2)
        grid_rates.addWidget(QtWid.QLabel("Hz"), 1, 2)
        grid_rates.setAlignment(QtCore.Qt.AlignTop)

        # 'Legend'
        self.legend_box = Legend_box(
            text=["saw+", "saw-", "sine+", "sine-"],
            pen=[PEN_01, PEN_02, PEN_03, PEN_04],
            checked=[False, True, True, True],
        )
        self.set_visibility_curves()
        for chkb in self.legend_box.chkbs:
            chkb.clicked.connect(self.set_visibility_curves)

        qgrp_legend = QtWid.QGroupBox("Legend")
        qgrp_legend.setStyleSheet(SS_GROUP)
        qgrp_legend.setLayout(self.legend_box.grid)

        # 'Chart'
        self.qpbt_pause_chart = QtWid.QPushButton("Pause", checkable=True)
        self.qpbt_pause_chart.clicked.connect(self.process_qpbt_pause_chart)
        self.qpbt_clear_chart = QtWid.QPushButton("Clear")
        self.qpbt_clear_chart.clicked.connect(self.process_qpbt_clear_chart)

        grid = QtWid.QGridLayout()
        grid.addWidget(self.qpbt_pause_chart, 0, 0)
        grid.addWidget(self.qpbt_clear_chart, 1, 0)
        grid.setAlignment(QtCore.Qt.AlignTop)

        qgrp_chart = QtWid.QGroupBox("Chart")
        qgrp_chart.setStyleSheet(SS_GROUP)
        qgrp_chart.setLayout(grid)

        vbox = QtWid.QVBoxLayout()
        vbox.addLayout(grid_rates)
        vbox.addWidget(qgrp_legend)
        vbox.addWidget(qgrp_chart)
        vbox.addStretch()

        # Round up frame
        hbox = QtWid.QHBoxLayout()
        hbox.addWidget(self.gw, 1)
        hbox.addLayout(vbox, 0)

        # -------------------------
        #   Round up full window
        # -------------------------

        vbox = QtWid.QVBoxLayout(self)
        vbox.addLayout(hbox, stretch=1)

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
            for tscurve in self.tscurves:
                tscurve.clear()

    @QtCore.pyqtSlot()
    def process_qpbt_pause_chart(self):
        if self.paused:
            self.qpbt_pause_chart.setText("Pause")
            self.paused = False
        else:
            self.qpbt_pause_chart.setText("Unpause")
            self.paused = True

    @QtCore.pyqtSlot()
    def update_GUI(self):
        self.qlbl_DAQ_rate.setText("%.1f" % qdev.obtained_DAQ_rate_Hz)

    @QtCore.pyqtSlot()
    def update_curves(self):
        for idx, tscurve in enumerate(self.tscurves):
            tscurve.update()
            
    @QtCore.pyqtSlot()
    def set_visibility_curves(self):
        for idx, tscurve in enumerate(self.tscurves):
            tscurve.set_visible(self.legend_box.chkbs[idx].isChecked())
            
    @QtCore.pyqtSlot()
    def update_charts(self):
        # Keep track of the obtained chart rate
        if not self.qet_chart.isValid():
            self.qet_chart.start()
        else:
            self.chart_rate_accumulator += 1
            dT = self.qet_chart.elapsed()

            if dT >= 1000:  # Evaluate every N elapsed milliseconds
                self.qet_chart.restart()
                try:
                    self.obtained_chart_rate_Hz = (
                        self.chart_rate_accumulator / dT * 1e3
                    )
                except ZeroDivisionError:
                    self.obtained_chart_rate_Hz = np.nan

                self.chart_rate_accumulator = 0

        self.qlbl_chart_rate.setText("%.1f" % self.obtained_chart_rate_Hz)
        self.plot_1.setTitle("%s points" % f"{(self.tscurve_1.size[0]):,}")

        if not self.paused:
            self.update_curves()


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


@QtCore.pyqtSlot()
def about_to_quit():
    qdev.quit()
    timer_chart.stop()


def DAQ_function():
    if window.tscurve_1.size[0] == 0:
        x_0 = 0
    else:
        x_0 = window.tscurve_1._buffer_x[-1]

    x = (1 + np.arange(WORKER_DAQ_INTERVAL_MS * Fs / 1e3)) / Fs + x_0
    y_saw = np.mod(x, 1)
    y_sine = np.sin(2 * np.pi * 0.5 * np.unwrap(x))

    window.tscurve_1.add_new_readings(x, y_saw)
    window.tscurve_2.add_new_readings(x, -y_saw)
    window.tscurve_3.add_new_readings(x, y_sine)
    window.tscurve_4.add_new_readings(x, -y_sine)

    return True


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtWid.QApplication(sys.argv)
    app.aboutToQuit.connect(about_to_quit)

    window = MainWindow()

    # Fake a device that generates data at a sampling rate of `Fs` Hz. The
    # data gets generated and transferred to our ChartHistory-instance from
    # out of a separate thread. This is taken care of by QDeviceIO.
    class FakeDevice:
        def __init__(self):
            self.name = "FakeDevice"
            self.is_alive = True

    qdev = QDeviceIO(dev=FakeDevice())
    qdev.create_worker_DAQ(
        DAQ_interval_ms=WORKER_DAQ_INTERVAL_MS, DAQ_function=DAQ_function
    )
    qdev.signal_DAQ_updated.connect(window.update_GUI)
    qdev.start()

    # Chart refresh timer
    timer_chart = QtCore.QTimer(timerType=QtCore.Qt.PreciseTimer)
    timer_chart.timeout.connect(window.update_charts)
    timer_chart.start(CHART_DRAW_INTERVAL_MS)

    window.show()
    sys.exit(app.exec_())
