#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mishmash of PyQt5 stylesheets and custom controls that I personally use in
many of my projects.


TODO:
    Add `toggle all/none` button to LegendBox. Make it optional.

    window.qpbt_show_all_curves = QtWid.QPushButton("toggle", maximumWidth=70)
    window.grid_show_curves.addWidget(
        window.qpbt_show_all_curves, N_channels, 0
    )
    window.qpbt_show_all_curves.clicked.connect(
        window.process_qpbt_show_all_curves
    )

    @QtCore.pyqtSlot()
    def process_qpbt_show_all_curves(self):
        # First: if any curve is hidden --> show all
        # Second: if all curves are shown --> hide all

        any_hidden = False
        for i_ in range(N_channels):
            if not self.chkbs_show_curves[i_].isChecked():
                self.chkbs_show_curves[i_].setChecked(True)
                any_hidden = True

        if not any_hidden:
            for i_ in range(N_channels):
                self.chkbs_show_curves[i_].setChecked(False)

    And don't forget to implement this in:
        dvg_device.Keysight_3497xA_demo_logger.py

"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/python-dvg-pyqt-controls"
__date__ = "31-07-2020"
__version__ = "1.0.0"

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QCheckBox

COLOR_RED = "rgb(255, 0, 0)"
COLOR_YELLOW = "rgb(255, 255, 0)"
COLOR_INDIAN_RED = "rgb(205, 92, 92)"
COLOR_SPRING_GREEN_2 = "rgb(0, 238, 118)"
COLOR_BISQUE_5 = "rgb(252, 208, 173)"
COLOR_READ_ONLY = "rgb(250, 230, 210)"

# Get the standard background color for a QButton from
# QtGui.QApplication.palette().button().color().name()
# However, at init there is no QApplication instance yet and Python crashes
# hence hard-code here.
COLOR_BTN_BG = "rgb(240, 240, 240)"

# ------------------------------------------------------------------------------
#   Style sheets
# ------------------------------------------------------------------------------
# fmt: off

SS_TEXTBOX_READ_ONLY = (
    "QLineEdit {"
        "border: 1px solid black}"

    "QLineEdit::read-only {"
        "border: 1px solid gray;"
        "background: " + COLOR_READ_ONLY + "}"

    "QPlainTextEdit {"
        "border: 1px solid black}"

    'QPlainTextEdit[readOnly="true"] {'
        "border: 1px solid gray;"
        "background-color: " + COLOR_READ_ONLY + "}"
)

SS_TEXTBOX_ERRORS = (
    "QLineEdit {"
        "border: 1px solid gray;"
        "background: " + COLOR_READ_ONLY + "}"

    "QLineEdit::read-only {"
        "border: 2px solid red;"
        "background: yellow;"
        "color: black}"

    "QPlainTextEdit {"
        "border: 1px solid gray;"
        "background-color: " + COLOR_READ_ONLY + "}"

    'QPlainTextEdit[readOnly="true"] {'
        "border: 2px solid red;"
        "background-color: yellow;"
        "color: black}"
)

SS_GROUP = (
    "QGroupBox {"
        "background-color: " + COLOR_BISQUE_5 + ";"
        "border: 2px solid gray;"
        "border-radius: 5px;"
        # "font: bold italic;"
        "font: bold;"
        "padding: 8 0 0 0px;"
        "margin-top: 2ex}"

    "QGroupBox::title {"
        "subcontrol-origin: margin;"
        # "subcontrol-position: top center;"
        "subcontrol-position: top left;"
        "padding: 0 3px}"

    "QGroupBox::flat {"
        "border: 0px;"
        "border-radius: 0 0px;"
        "padding: 0}"
)

SS_GROUP_BORDERLESS = (
    "QGroupBox {"
        "border: 0px solid gray;"
        "border-radius: 5px;"
        # "font: bold italic;"
        "font: bold;"
        "padding: 0 0 0 0px;"
        "margin-top: 0ex}"

    "QGroupBox::title {"
        "subcontrol-origin: margin;"
        # "subcontrol-position: top center;"
        "subcontrol-position: top left;"
        "padding: 0 0px}"

    "QGroupBox::flat {"
        "border: 0px;"
        "border-radius: 0 0px;"
        "padding: 0}"
)

SS_LED = (
    "QPushButton {"
        "background-color: " + COLOR_INDIAN_RED + ";"
        "border-style: inset;"
        "border-width: 1px;"
        "min-height: 30px;"
        "min-width: 30px;"
        "max-width: 30px}"

    "QPushButton::disabled {"
        "border-radius: 15px;"
        "color: black}"

    "QPushButton::checked {"
        "background-color: " + COLOR_SPRING_GREEN_2 + ";"
        "border-style: outset}"
)

SS_LED_RECT = (
    "QPushButton {"
        "background-color: " + COLOR_INDIAN_RED + ";"
        "border-style: solid;"
        "border-width: 1px;"
        "min-height: 30px;"
        "min-width: 76px;"
        "max-width: 76px}"

    "QPushButton::disabled {"
        "border-radius: 1px;"
        "color: black}"

    "QPushButton::checked {"
        "background-color: " + COLOR_SPRING_GREEN_2 + "}"
)

SS_ERROR_LED = (
    "QPushButton {"
        "background-color: " + COLOR_SPRING_GREEN_2 + ";"
        "border: 1px solid gray;"
        "min-height: 30px;"
        "min-width: 30px}"

    "QPushButton::disabled {"
        "color: black}"

    "QPushButton::checked {"
        "font-weight: bold;"
        "background-color: red}"
)

SS_TINY_ERROR_LED = (
    "QPushButton {"
        "background-color: " + COLOR_BTN_BG + ";"
        "border-style: inset;"
        "border-width: 1px;"
        "max-height: 10px;"
        "max-width: 10px;"
        "height: 10px;"
        "width: 10px}"

    "QPushButton::disabled {"
        "border-radius: 5px;"
        "color: black}"

    "QPushButton::checked {"
        "background-color: red;"
        "border-style: outset}"
)

SS_TINY_LED = (
    "QPushButton {"
        "background-color: " + COLOR_BTN_BG + ";"
        "border-style: inset;"
        "border-width: 1px;"
        "max-height: 10px;"
        "max-width: 10px;"
        "height: 10px;"
        "width: 10px}"

    "QPushButton::disabled {"
        "border-radius: 5px;"
        "color: black}"

    "QPushButton::checked {"
        "background-color: " + COLOR_SPRING_GREEN_2 + ";"
        "border-style: outset}"
)

SS_TEXT_MSGS = (
    "QPlainTextEdit::disabled {"
        "color: black;"
        "background-color: white}"
)

SS_TITLE = (
    "QLabel {"
        "background-color: " + COLOR_BISQUE_5 + ";"
        "font: bold}"
)

# fmt: on
# -----------------------------------------------------------------------------
#   LegendBox
# -----------------------------------------------------------------------------


class LegendBox(QWidget):
    def __init__(
        self,
        text="",
        pen=QtGui.QPen(QtCore.Qt.red),
        checked=True,
        bg_color=QtGui.QColor(36, 36, 36),
        box_width=40,
        box_height=23,
        parent=None,
    ):
        super().__init__(parent=parent)

        if not isinstance(text, list):
            text = [text]
        if not isinstance(pen, list):
            pen = [pen]
        if not isinstance(checked, list):
            checked = [checked]

        self.chkbs = []
        self.painted_lines = []
        self.grid = QGridLayout(spacing=1)

        for i in range(len(text)):
            try:
                _checked = checked[i]
            except:  # pylint: disable=bare-except
                _checked = True

            chkb = QCheckBox(
                text[i], layoutDirection=QtCore.Qt.LeftToRight, checked=_checked
            )
            self.chkbs.append(chkb)

            PaintedLine = self.PaintedLine(
                pen[i], bg_color, box_width, box_height
            )
            self.painted_lines.append(PaintedLine)

            p = {"alignment": QtCore.Qt.AlignLeft}
            self.grid.addWidget(chkb, i, 0, **p)
            self.grid.addWidget(PaintedLine, i, 1)
            self.grid.setColumnStretch(0, 0)
            self.grid.setColumnStretch(1, 1)
            self.grid.setAlignment(QtCore.Qt.AlignTop)

    class PaintedLine(QWidget):
        def __init__(self, pen, bg_color, box_width, box_height, parent=None):
            super().__init__(parent=parent)

            self.pen = pen
            self.bg_color = bg_color
            self.box_width = box_width
            self.box_height = box_height

            self.setFixedWidth(box_width)
            self.setFixedHeight(box_height)

        def paintEvent(self, _event):
            w = self.width()
            h = self.height()
            x = 8
            y = 6

            painter = QtGui.QPainter()
            painter.begin(self)
            painter.fillRect(0, 0, w, h, self.bg_color)
            painter.setPen(self.pen)
            painter.drawLine(QtCore.QLine(x, h - y, w - x, y))
            painter.end()


# -----------------------------------------------------------------------------
#   Create controls
# -----------------------------------------------------------------------------


def create_Toggle_button_style_sheet(
    bg_clr=COLOR_BTN_BG,
    color="black",
    checked_bg_clr=COLOR_SPRING_GREEN_2,
    checked_color="black",
    checked_font_weight="normal",
) -> str:
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + bg_clr + ";"
            "color: " + color + ";"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 4px;"
            "border-color: gray;"
            "text-align: center;"
            "padding: 1px 1px 1px 1px;}"

        "QPushButton:disabled {"
            "color: black;}"

        "QPushButton:checked {"
            "background-color: " + checked_bg_clr + ";"
            "color: " + checked_color + ";"
            "font-weight: " + checked_font_weight + ";"
            "border-style: inset;}"
    )
    # fmt: on
    return SS


def create_LED_indicator() -> QPushButton:
    button = QPushButton(text="0", checkable=True, enabled=False)
    button.setStyleSheet(SS_LED)
    return button


def create_LED_indicator_rect(initial_state=False, text="") -> QPushButton:
    button = QPushButton(text=text, checkable=True, enabled=False)
    button.setStyleSheet(SS_LED_RECT)
    button.setChecked(initial_state)
    return button


def create_Relay_button() -> QPushButton:
    button = QPushButton(text="0", checkable=True)
    button.setStyleSheet(SS_LED)
    return button


def create_Toggle_button(text="", minimumHeight=40) -> QPushButton:
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_BTN_BG + ";"
            "color: black;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 4px;"
            "border-color: gray;"
            "text-align: center;"
            "padding: 1px 1px 1px 1px;}"

        "QPushButton:disabled {"
            "color: grey;}"

        "QPushButton:checked {"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";"
            "color: black;" + "font-weight: normal;"
            "border-style: inset;}"
    )
    # fmt: on
    button = QPushButton(text=text, checkable=True)
    button.setStyleSheet(SS)

    if minimumHeight is not None:
        button.setMinimumHeight(minimumHeight)

    return button


def create_Toggle_button_2(text="", minimumHeight=40) -> QPushButton:
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_BTN_BG + ";"
            "color: black;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 4px;"
            "border-color: gray;"
            "text-align: center;"
            "padding: 1px 1px 1px 1px;}"

        "QPushButton:disabled {"
            "color: grey;}"

        "QPushButton:checked {"
            "background-color: " + COLOR_YELLOW + ";"
            "color: black;" + "font-weight: bold;"
            "border-color: red;"
            "border-style: inset;}"
    )
    # fmt: on
    button = QPushButton(text=text, checkable=True)
    button.setStyleSheet(SS)

    if minimumHeight is not None:
        button.setMinimumHeight(minimumHeight)

    return button


def create_Toggle_button_3(text="", minimumHeight=40) -> QPushButton:
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_YELLOW + ";"
            "color: black;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 4px;"
            "border-color: red;"
            "text-align: center;"
            "font-weight: bold;"
            "padding: 1px 1px 1px 1px;}"

        "QPushButton:disabled {"
            "color: grey;}"

        "QPushButton:checked {"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";"
            "color: black;" + "border-color: gray;"
            "border-style: inset;"
            "font-weight: normal;}"
    )
    # fmt: on
    button = QPushButton(text=text, checkable=True)
    button.setStyleSheet(SS)

    if minimumHeight is not None:
        button.setMinimumHeight(minimumHeight)

    return button


def create_tiny_error_LED(text="") -> QPushButton:
    button = QPushButton(text=text, checkable=True, enabled=False)
    button.setStyleSheet(SS_TINY_ERROR_LED)
    return button


def create_tiny_LED(text="") -> QPushButton:
    button = QPushButton(text=text, checkable=True, enabled=False)
    button.setStyleSheet(SS_TINY_LED)
    return button


def create_error_LED(text="") -> QPushButton:
    button = QPushButton(text=text, checkable=True, enabled=False)
    button.setStyleSheet(SS_ERROR_LED)
    return button
