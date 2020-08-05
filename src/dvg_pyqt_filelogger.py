#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class FileLogger handles logging data to file, particularly well suited for
multithreaded programs, where one thread is writing data to the log (the logging
thread) and the other thread (the main thread/GUI) handles starting and stopping
of the logging by user interaction (i.e. a button).

The functions 'start_recording' and 'stop_recording' should be directly called
from the main/GUI thread.

In the logging thread one should test for the following booleans as demonstrated
in the following example:
    if file_logger.starting:
        if file_logger.create_log(my_current_time, my_path):
            file_logger.write("Time\tValue\n")  # Header

    if file_logger.stopping:
        file_logger.close()

    if file_logger.is_recording:
        elapsed_time = my_current_time - file_logger.start_time
        file_logger.write("%.3f\t%.3f\n" % (elapsed_time, my_value))

Class:
    FileLogger():
        Methods:
            start_recording():
                Prime the start of recording.
            stop_recording():
                Prime the stop of recording.
            create_log(...):
                Open new log file and keep file handle open.
            write(...):
                Write data to the open log file.
            close():
                Close the log file.

        Important members:
            starting (bool):
            stopping (bool):
            is_recording (bool):

        Signals:
            signal_set_recording_text(str):
                Useful for updating text of e.g. a record button when using a
                PyQt GUI. This signal is not emitted in this module itself, and
                you should emit it yourself in your own code when needed.
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/..."
__date__ = "05-08-2020"
__version__ = "1.0.0"
# NOTE: No mutex implemented here! Notify the user.
# NOTE: Everything in this module will run in the Worker_DAQ thread! We need to
# signal any changes we want to the GUI.
# NOTE: Module will struggle on by design when exceptions occur. They are only
# reported to the command line and the module will continue on.

from pathlib import Path
from typing import AnyStr, Callable

from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime

from dvg_debug_functions import print_fancy_traceback as pft


class FileLogger(QtCore.QObject):
    signal_recording_started = QtCore.pyqtSignal(str)
    signal_recording_stopped = QtCore.pyqtSignal(Path)

    def __init__(
        self,
        write_header_fun: Callable = None,
        write_data_fun: Callable = None,
    ):
        """
        Instruct user that he should use:
            * self.write()`

        Optionally:
            * self.elapsed() # For PC timestamp, taken from time.perf_counter()
        """
        super().__init__(parent=None)

        self._write_header_fun = write_header_fun
        self._write_data_fun = write_data_fun

        self._filepath = None  # Will be of type pathlib.Path()
        self._filehandle = None
        self._mode = "a"

        self._timer = QtCore.QElapsedTimer()
        self._is_starting = False
        self._is_stopping = False
        self._is_recording = False

    def __del__(self):
        if self._is_recording:
            self._filehandle.close()

    def set_write_header_fun(self, write_header_fun: Callable):
        """
        Instruct user that he should use:
            * self.write()
        """
        self._write_header_fun = write_header_fun

    def set_write_data_fun(self, write_data_fun: Callable):
        """
        Instruct user that he should use:
            * self.write()`

        Optionally:
            * self.elapsed() # For PC timestamp, taken from time.perf_counter()
        """
        self._write_data_fun = write_data_fun

    def record(self, state):
        """Convenience function
        """
        if state:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self._is_starting = True
        self._is_stopping = False

    def stop_recording(self):
        self._is_starting = False
        self._is_stopping = True

    def update(self, filepath: str == "", mode: str = "a"):
        """
            mode (str):
                Mode in which the file is openend, see 'open()' for more
                details. Defaults to 'a'. Most common options:
                'w': Open for writing, truncating the file first
                'a': Open for writing, appending to the end of the file if it
                     exists
        """
        if self._is_starting:
            if filepath == "":
                filepath = (
                    QDateTime.currentDateTime().toString("yyMMdd_HHmmss")
                    + ".txt"
                )

            self._filepath = Path(filepath)
            self._mode = mode

            # Reset flags
            self._is_starting = False
            self._is_stopping = False

            if self._create_log():
                self.signal_recording_started.emit(filepath)
                self._is_recording = True
                if self._write_header_fun is not None:
                    self._write_header_fun()
                self._timer.start()

            else:
                self._is_recording = False

        if self._is_stopping:
            self.signal_recording_stopped.emit(self._filepath)
            self._timer.invalidate()
            self.close()

        if self._is_recording:
            if self._write_data_fun is not None:
                self._write_data_fun()

    def elapsed(self) -> float:
        """
        Returns time in seconds since start of recording.
        """
        return self._timer.elapsed() / 1e3

    def _create_log(self) -> bool:
        """Open new log file and keep file handle open.
        Returns:
            True if successful, False otherwise.
        """
        try:
            self._filehandle = open(self._filepath, self._mode)
        except Exception as err:  # pylint: disable=broad-except
            pft(err, 3)
            self._is_recording = False
            return False
        else:
            self._is_recording = True
            return True

    def write(self, data: AnyStr) -> bool:
        """
        Returns:
            True if successful, False otherwise.
        """
        try:
            self._filehandle.write(data)
        except Exception as err:  # pylint: disable=broad-except
            pft(err, 3)
            return False
        else:
            return True

    def flush(self):
        """Force-flush the contents in the OS buffer to file as soon as
        possible. Do not call repeatedly, because it causes overhead.
        """
        self._filehandle.flush()

    def close(self):
        """
        """
        if self._is_recording:
            self._filehandle.close()
        self._is_starting = False
        self._is_stopping = False
        self._is_recording = False

