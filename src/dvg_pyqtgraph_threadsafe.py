#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class ChartHistory provides a thread-safe history buffer for (x, y)-data
points behind a PyQtGraph plot curve. Hence, the plot curve can now act as a
history strip chart or Lissajous chart, whilst being fed with new data.

TODO: Only strip charts -- with the x-array always being shifted such that
the right side is 0 -- are supported at the moment. I should implement
a toggle for enabling/disabling this shift, such that Lissajous curves
are also possible.

TODO: All thread-safe:
History Chart, buffered, with x-data shifted such that right-side always == 0
Buffered Plot, buffered, (x, y)-data as is, can also support Lissajous
Plot, unbuffered, (x, y)-data as is (Note: was originally named DvG_pyqt_BufferedPlot.py)
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/..."
__date__ = "22-07-2020"
__version__ = "1.0.0"

import numpy as np
from PyQt5 import QtCore
import pyqtgraph as pg

from dvg_ringbuffer import RingBuffer


class ThreadSafeCurve(object):
    def __init__(
        self,
        capacity: int,
        linked_curve: pg.PlotDataItem,
        shift_right_x_to_zero: bool = True,
        use_ringbuffer: bool = True,
    ):
        """Provides a thread-safe buffer for (x, y)-data points behind a
        PyQtGraph plot curve. Hence, the plot curve can now act as a time-moving
        strip chart or Lissajous chart.

        The history buffer consists of two ring buffers of fixed capacity.
        New readings are placed at the end (right-side) of the array, pushing
        out the oldest readings when the buffer has reached its maximum capacity
        (FIFO).

        This class is thread-safe. Intended multithreaded operation: One thread
        does the data acquisition and pushes new data points into the history
        buffer by calling `add_new_reading(s)()`. Another thread performs the
        GUI refresh by calling `update_curve()` which will redraw the curve.

        Args:
            capacity (int):
                Max. number of (x, y)-data points the history buffer can store.

            linked_curve (:class:`pyqtgraph.PlotDataItem`):
                Instance of :class:`pyqtgraph.PlotDataItem` to plot the buffered
                data out into.

        Attributes:
            x_axis_divisor (float):
                The x-data in the history buffer will be divided by this factor
                when the plot curve is redrawn. Useful to, e.g., transform the
                x-axis units from milliseconds to seconds or minutes.

                Default: 1

            y_axis_divisor (float):
                Same functionality as x_axis_divisor.

                Default: 1
        """
        self.capacity = capacity
        self.curve = linked_curve
        self._shift_right_x_to_zero = shift_right_x_to_zero
        self._use_ringbuffer = use_ringbuffer
        self._mutex = QtCore.QMutex()  # To allow proper multithreading

        self.x_axis_divisor = 1
        self.y_axis_divisor = 1

        if self._use_ringbuffer:
            self._buffer_x = RingBuffer(capacity=capacity)
            self._buffer_y = RingBuffer(capacity=capacity)
        else:
            self._buffer_x = np.array([])
            self._buffer_y = np.array([])

        self._snapshot_x = [0]
        self._snapshot_y = [0]

        if self.curve is not None:
            # Performance boost: Do not plot data outside of visible range
            self.curve.clipToView = True

            # Default to no downsampling
            self.curve.setDownsampling(ds=1, auto=False, method="mean")

    def apply_downsampling(self, do_apply: bool = True, ds=4):
        """Downsample the curve by using PyQtGraph's build-in method.
        """
        if self.curve is not None:
            if do_apply:
                # Speed up plotting, needed for keeping the GUI responsive when
                # using large datasets
                self.curve.setDownsampling(ds=ds, auto=False, method="mean")
            else:
                self.curve.setDownsampling(ds=1, auto=False, method="mean")

    def add_new_reading(self, x, y):
        """Add a single (x, y)-data point to the ring buffer.
        """
        if self._use_ringbuffer:
            locker = QtCore.QMutexLocker(self._mutex)
            self._buffer_x.append(x)
            self._buffer_y.append(y)
            locker.unlock()

    def add_new_readings(self, x_list, y_list):
        """Add a list of (x, y)-data points to the ring buffer.
        """
        if self._use_ringbuffer:
            locker = QtCore.QMutexLocker(self._mutex)
            self._buffer_x.extend(x_list)
            self._buffer_y.extend(y_list)
            locker.unlock()

    def set_data(self, x_list, y_list):
        """Set the (x, y)-data underlying the curve.
        """
        if not self._use_ringbuffer:
            locker = QtCore.QMutexLocker(self._mutex)
            self._buffer_x = x_list
            self._buffer_y = y_list
            locker.unlock()

    def update(self):
        """Update the data behind the curve, based on the current contents of
        the history buffer, and redraw the curve on screen.
        """

        # Create a snapshot of the buffered data. Fast operation.
        locker = QtCore.QMutexLocker(self._mutex)
        self._snapshot_x = np.copy(self._buffer_x)
        self._snapshot_y = np.copy(self._buffer_y)
        # print("numel x: %d, numel y: %d" %
        #      (self._snapshot_x.size, self._snapshot_y.size))
        locker.unlock()

        # Now update the data behind the curve and redraw it on screen.
        # Note: .setData() is a super fast operation and will internally emit
        # a PyQt signal to redraw the curve, once it has updated its data
        # members. That's why .setData() returns almost immediately, but the
        # curve still has to get redrawn.
        if self.curve is not None:
            if (len(self._snapshot_x) == 0) or (
                np.alltrue(np.isnan(self._snapshot_y))
            ):
                self.curve.setData([], [])
            else:
                x_0 = self._snapshot_x[-1] if self._shift_right_x_to_zero else 0
                self.curve.setData(
                    (self._snapshot_x - x_0) / float(self.x_axis_divisor),
                    self._snapshot_y / float(self.y_axis_divisor),
                )

    def clear(self):
        """Clear the contents of the curve and redraw.
        """
        locker = QtCore.QMutexLocker(self._mutex)
        if self._use_ringbuffer:
            self._buffer_x.clear()
            self._buffer_y.clear()
        else:
            self._buffer_x = np.array([])
            self._buffer_y = np.array([])
        locker.unlock()

        self.update()
        
    def set_visible(self, state: bool = True):
        self.curve.setVisible(state)

    @property
    def size(self):
        """Number of elements currently contained in the underlying (x, y)-
        buffers of the curve. Note that this is not neccesarily the number of
        elements of the currently drawn curve, but reflects the data buffer
        behind it that will be drawn onto screen by the next call to
        `update_curve()`.
        """
        # fmt: off
        locker = QtCore.QMutexLocker(self._mutex) # pylint: disable=unused-variable
        # fmt: on
        return (len(self._buffer_x), len(self._buffer_y))


class HistoryChartCurve(ThreadSafeCurve):
    def __init__(self, capacity: int, linked_curve: pg.PlotDataItem = None):
        """
        """
        super().__init__(
            capacity=capacity,
            linked_curve=linked_curve,
            shift_right_x_to_zero=True,
            use_ringbuffer=True,
        )


class BufferedPlotCurve(ThreadSafeCurve):
    def __init__(self, capacity: int, linked_curve: pg.PlotDataItem = None):
        """
        """
        super().__init__(
            capacity=capacity,
            linked_curve=linked_curve,
            shift_right_x_to_zero=False,
            use_ringbuffer=True,
        )


class PlotCurve(ThreadSafeCurve):
    def __init__(self, capacity: int, linked_curve: pg.PlotDataItem = None):
        """
        """
        super().__init__(
            capacity=capacity,
            linked_curve=linked_curve,
            shift_right_x_to_zero=False,
            use_ringbuffer=False,
        )
