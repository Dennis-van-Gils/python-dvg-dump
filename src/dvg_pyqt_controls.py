#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mishmash of PyQt5 stylesheets and custom controls that I personally use in
many of my projects.
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/python-dvg-pyqt-controls"
__date__ = "04-08-2020"
__version__ = "1.0.0"

from PyQt5.QtWidgets import QPushButton

COLOR_INDIAN_RED_2 = "rgb(225, 102, 102)"
COLOR_SPRING_GREEN_2 = "rgb(0, 238, 118)"
COLOR_BISQUE_5 = "rgb(252, 218, 183)"
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
        "padding: 0 2px;"
        "border: 1px solid black}"

    "QLineEdit:read-only {"
        "border: 1px solid dimgray;"
        "background: " + COLOR_READ_ONLY + "}"

    "QPlainTextEdit {"
        "border: 1px solid black}"

    'QPlainTextEdit[readOnly="true"] {'
        "border: 1px solid dimgray;"
        "background-color: " + COLOR_READ_ONLY + "}"
)

SS_TEXTBOX_ERRORS = (
    "QLineEdit {"
        "padding: 0 2px;"
        "border: 1px solid dimgray;"
        "background: " + COLOR_READ_ONLY + "}"

    "QLineEdit::read-only {"
        "border: 2px solid red;"
        "background: yellow;"
        "color: black}"

    "QPlainTextEdit {"
        "border: 1px solid dimgray;"
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
        "font: bold;"
        "padding: 8 0 0 0px;"
        "margin-top: 2ex}"

    "QGroupBox::title {"
        "subcontrol-origin: margin;"
        "subcontrol-position: top left;"
        "padding: 0 3px}"

    "QGroupBox::flat {"
        "border: 0px;"
        "border-radius: 0 0px;"
        "padding: 0}"
)

SS_TITLE = (
    "QLabel {"
        "background-color: " + COLOR_BISQUE_5 + ";"
        "padding: 10px;"
        "border-radius: 5px;"
        "font: bold}"
)
# fmt: on

# ------------------------------------------------------------------------------
#   LEDs
# ------------------------------------------------------------------------------


def create_LED_indicator(**kwargs) -> QPushButton:
    """
    False: dim red
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_INDIAN_RED_2 + ";"
            "color: black;"
            "border: 1px solid black;"
            "border-radius: 15px;"
            "max-height: 30 px;"
            "max-width: 30 px;"
            "height: 30px;"
            "width: 30px;}"

        "QPushButton::checked {"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";}"
    )
    # fmt: on
    button = QPushButton(checkable=True, enabled=False, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_LED_indicator_rect(**kwargs) -> QPushButton:
    """
    False: dim red
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_INDIAN_RED_2 + ";"
            "color: black;"
            "border: 1px solid black;"
            "border-radius: 0px;"
            "min-height: 30px;"
            "min-width: 76px;}"

        "QPushButton::checked {"
            "background-color: " + COLOR_SPRING_GREEN_2 + "}"
    )
    # fmt: on
    button = QPushButton(checkable=True, enabled=False, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_error_LED(**kwargs) -> QPushButton:
    """
    False: green
    True : red
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";"
            "color: black;"
            "border: 1px solid black;"
            "border-radius: 0px;"
            "min-height: 30px;"
            "min-width: 30px}"

        "QPushButton::checked {"
            "font-weight: bold;"
            "background-color: red}"
    )
    # fmt: on
    button = QPushButton(checkable=True, enabled=False, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_tiny_LED(**kwargs) -> QPushButton:
    """
    False: default
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_BTN_BG + ";"
            "color: black;"
            "border: 1px solid black;"
            "border-radius: 5px;"
            "max-height: 10 px;"
            "max-width: 10 px;"
            "height: 10px;"
            "width: 10px;}"

        "QPushButton::checked {"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";}"
    )
    # fmt: on
    button = QPushButton(checkable=True, enabled=False, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_tiny_error_LED(**kwargs) -> QPushButton:
    """
    False: default
    True : red
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "background-color: " + COLOR_BTN_BG + ";"
            "color: black;"
            "border: 1px solid black;"
            "border-radius: 5px;"
            "max-height: 10 px;"
            "max-width: 10 px;"
            "height: 10px;"
            "width: 10px;}"

        "QPushButton::checked {"
            "background-color: red;}"
    )
    # fmt: on
    button = QPushButton(checkable=True, enabled=False, **kwargs)
    button.setStyleSheet(SS)
    return button


# ------------------------------------------------------------------------------
#   Toggle buttons
# ------------------------------------------------------------------------------

DFLT_TOGGLE_BTN_PADDING = "6px 6px 6px 6px"
DFLT_TOGGLE_BTN_BORDER_STYLE = "outset"
DFLT_TOGGLE_BTN_BORDER_STYLE_CHECKED = "inset"
DFLT_TOGGLE_BTN_BORDER_WIDTH = "2px"
DFLT_TOGGLE_BTN_BORDER_RADIUS = "4px"


def create_Relay_button(**kwargs) -> QPushButton:
    """
    False: dim red
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "border-style: inset;"
            "border-width: 1px;"
            "max-height: 30 px;"
            "max-width: 30 px;"
            "height: 30px;"
            "width: 30px;"
            "background-color: " + COLOR_INDIAN_RED_2 + ";}"

        "QPushButton:disabled {"
            "border: 1px solid black;"
            "border-radius: 15px;"
            "color: black;}"

        "QPushButton:checked {"
            "border-style: outset;"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";}"
    )
    # fmt: on
    button = QPushButton(checkable=True, **kwargs)
    button.setStyleSheet(SS)

    # NOTE: Do not enable below code. There is a good reason to not change the
    # relay button label immediately at click. The text-value "0" or "1" can
    # better be set after the relay operation was deemed successful by the main
    # program.
    #
    # def set_text_clicked(button):
    #    button.setText("1" if button.isChecked() else "0")
    # button.clicked.connect(lambda: set_text_clicked(button))
    # set_text_clicked(button)

    return button


def create_Toggle_button(**kwargs) -> QPushButton:
    """
    False: default
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "padding: " + DFLT_TOGGLE_BTN_PADDING + ";"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE + ";"
            "border-width: " + DFLT_TOGGLE_BTN_BORDER_WIDTH + ";"
            "border-radius: " + DFLT_TOGGLE_BTN_BORDER_RADIUS + ";"
            "border-color: dimgray;"
            "color: black;"
            "background-color: " + COLOR_BTN_BG + ";}"

        "QPushButton:disabled {"
            "color: dimgray;}"

        "QPushButton:checked {"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE_CHECKED + ";"
            "font-weight: normal;"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";}"
    )
    # fmt: on
    button = QPushButton(checkable=True, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_Toggle_button_2(**kwargs) -> QPushButton:
    """
    False: default
    True : warning red-lined yellow
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "padding: " + DFLT_TOGGLE_BTN_PADDING + ";"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE + ";"
            "border-width: " + DFLT_TOGGLE_BTN_BORDER_WIDTH + ";"
            "border-radius: " + DFLT_TOGGLE_BTN_BORDER_RADIUS + ";"
            "border-color: dimgray;"
            "color: black;"
            "background-color: " + COLOR_BTN_BG + ";}"

        "QPushButton:disabled {"
            "color: dimgray;}"

        "QPushButton:checked {"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE_CHECKED + ";"
            "border-color: red;"
            "font-weight: bold;"
            "background-color: yellow;}"
    )
    # fmt: on
    button = QPushButton(checkable=True, **kwargs)
    button.setStyleSheet(SS)
    return button


def create_Toggle_button_3(**kwargs) -> QPushButton:
    """
    False: warning red-lined yellow
    True : green
    """
    # fmt: off
    SS = (
        "QPushButton {"
            "padding: " + DFLT_TOGGLE_BTN_PADDING + ";"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE + ";"
            "border-width: " + DFLT_TOGGLE_BTN_BORDER_WIDTH + ";"
            "border-radius: " + DFLT_TOGGLE_BTN_BORDER_RADIUS + ";"
            "border-color: red;"
            "color: black;"
            "font-weight: bold;"
            "background-color: yellow;}"

        "QPushButton:disabled {"
            "color: dimgray;}"

        "QPushButton:checked {"
            "border-style: " + DFLT_TOGGLE_BTN_BORDER_STYLE_CHECKED + ";"
            "border-color: dimgray;"
            "font-weight: normal;"
            "background-color: " + COLOR_SPRING_GREEN_2 + ";}"
    )
    # fmt: on
    button = QPushButton(checkable=True, **kwargs)
    button.setStyleSheet(SS)
    return button
