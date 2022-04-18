import os
import sys

from config import Config

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStatusBar, QLabel, \
    QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QComboBox, QLineEdit, QSpinBox, QMessageBox, QApplication


class View(QMainWindow):
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    app_name = "HighResMS m/z calculator"
    font = QFont("Montserrat")

    icon_path = ["assets", "images", "icon_red.jpg"]
    icon_image= resource_path(os.path.join(*icon_path))

    icon2_path = ["assets", "images", "icon2.jpg"]
    icon2_image= resource_path(os.path.join(*icon2_path))

    not_found_path = ["assets", "images", "not_found.png"]
    not_found_image= resource_path(os.path.join(*not_found_path))

    delete_icon_path = ["assets", "images", "delete_list.png"]
    delete_image= resource_path(os.path.join(*delete_icon_path))

    btn_icon_path = ["assets", "images", "icon.png"]
    btn_image= resource_path(os.path.join(*btn_icon_path))

    def __init__(self):
        super().__init__()
        self.central_layout = QWidget()
        self.central_layout.setFont(self.font)
        self.setCentralWidget(self.central_layout)
        self.setWindowTitle("HighResMS m/z calculator")
        self.setStyleSheet("background-color: white;"
                           "font-size: 14pt;")
        self.resize(650, 650)
        self.setWindowIcon(QtGui.QIcon(self.icon_image))

        self.main_layout = QVBoxLayout()
        self.central_layout.setLayout(self.main_layout)
        self._create_status_bar()
        self.calculate_btn()
        self._display_top()
        self._create_menu()
        self.optional_info()
        self._display_logger()

    def _create_status_bar(self):
        status = QStatusBar()
        status.setStyleSheet("font-size: 8pt; background-color: lightgrey;")
        self.description = QLabel(f"This is the {self.app_name} software. Version 0.9")
        status.addPermanentWidget(self.description, 0)

        self.app_status = QStatusBar()
        self.app_status.showMessage("Feel free to play")
        status.addWidget(self.app_status)

        self.setStatusBar(status)

    def _create_menu(self):
        self.topbar = self.menuBar()
        self.menu = self.topbar.addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)
        self.topbar.addAction('&Instructions', self.pop_up_instructions)
        self.topbar.addAction('&About', self.pop_up_about)

    def _display_top(self):
        fixed_bar = QHBoxLayout()
        fixed_bar.setContentsMargins(10, 10, 10, 10)
        fixed_bar.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        fixed_bar.setSpacing(35)

        input_formula_display = QVBoxLayout()
        input_formula_display.setSpacing(5)
        input_formula_label = QLabel("Targeted formula")
        input_formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.target_formula = QLineEdit(placeholderText="Insert here")
        self.target_formula.setFont(self.font)
        self.target_formula.setFixedSize(170, 40)
        input_formula_display.addWidget(input_formula_label)
        input_formula_display.addWidget(self.target_formula)

        adduct_display = QVBoxLayout()
        adduct_display.setSpacing(5)
        adduct_label = QLabel("Adduct")
        adduct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adduct_list = QComboBox()
        self.adduct_list.addItems(list(Config.adducts.keys()))
        self.adduct_list.setFixedSize(170, 40)
        adduct_display.addWidget(adduct_label)
        adduct_display.addWidget(self.adduct_list)

        charge_display = QVBoxLayout()
        charge_display.setSpacing(5)
        charge_label = QLabel("Charge")
        charge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.charge_list = QSpinBox()
        self.charge_list.setMinimum(-10)
        self.charge_list.setMaximum(+10)
        self.charge_list.setFixedSize(170, 40)
        charge_display.addWidget(charge_label)
        charge_display.addWidget(self.charge_list)

        fixed_bar.addLayout(input_formula_display)
        fixed_bar.addLayout(adduct_display)
        fixed_bar.addLayout(charge_display)

        self.main_layout.addLayout(fixed_bar)

    def optional_info(self):
        optional_box_layout = QVBoxLayout()
        optional_box_layout.setContentsMargins(30, 0, 30, 10)

        aditional_info_label = QLabel("Aditional information")
        aditional_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.optional_box = QHBoxLayout()
        self.optional_box = QLineEdit(placeholderText="Optional (e.g. Compound name).")
        self.optional_box.setFont(self.font)
        self.optional_box.setFixedHeight(40)
        optional_box_layout.addWidget(aditional_info_label)
        optional_box_layout.addWidget(self.optional_box)

        self.main_layout.addLayout(optional_box_layout)

    def calculate_btn(self):
        calculate_btn_display = QHBoxLayout()
        calculate_btn_display.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.calculate_btn = QPushButton('   CALCULATE m/z')
        self.calculate_btn.setIcon(QtGui.QIcon(self.btn_image))
        self.calculate_btn.setIconSize(QSize(50,50))
        self.calculate_btn.setFixedSize(270, 75)
        calculate_btn_display.addWidget(self.calculate_btn)

        self.delete_logger_btn = QPushButton('   Restart data')
        self.delete_logger_btn.setIcon(QtGui.QIcon(self.delete_image))
        self.delete_logger_btn.setIconSize(QSize(50,50))
        self.delete_logger_btn.setFixedSize(270, 75)
        calculate_btn_display.addWidget(self.delete_logger_btn)

        self.main_layout.addLayout(calculate_btn_display)


    def _display_logger(self):
        logger_box = QVBoxLayout()
        logger_box.setContentsMargins(30, 0, 30, 10)

        logger_title = QLabel("RESULTS")
        logger_title.setStyleSheet("color: black;"
                                   "font: bold;")
        logger_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.logger_display = QTextEdit()
        self.logger_display.setReadOnly(True)
        self.logger_display.setStyleSheet("background-color : white; "
                                          "font-size: 10pt;"
                                          "border-style: outset;"
                                          "border-width: 1px;"
                                          "font: arial")

        logger_box.addWidget(logger_title)
        logger_box.addWidget(self.logger_display)

        self.main_layout.addLayout(logger_box)

    def print_logger(self, text):
        self.logger_display.append(text)
        self.target_formula.clear()
        self.optional_box.clear()

    def get_formula_name(self):
        return self.target_formula.text()

    def get_aditional_info(self):
        return self.optional_box.text()

    def get_selected_charge(self):
        return self.charge_list.text()

    def get_selected_adduct(self):
        return self.adduct_list.currentText()

    def clear_data_list(self):
        return self.logger_display.clear()

    def not_found_element_pop_up(self):
        self.not_found_box = QMessageBox()
        not_found_image= QtGui.QPixmap(self.not_found_image)
        not_found_image.scaled(10,10)

        self.not_found_box.setIconPixmap(not_found_image.scaled(200,200))
        self.not_found_box.setWindowIcon(QtGui.QIcon(self.icon_image))
        self.not_found_box.setWindowTitle("Invalid formula")
        self.not_found_box.setText("\n\nPlease, try using a valid formula.")
        mss_box_font = self.font
        mss_box_font.setPointSize(20)
        self.not_found_box.setFont(mss_box_font)
        self.not_found_box.StandardButton.Ok
        self.target_formula.clear()
        self.not_found_box.exec()

    def pop_up_instructions(self):
        self.pop_up_instructions_box = QMessageBox()
        instructions_image= QtGui.QPixmap(self.icon2_image)
        instructions_image.scaled(10,10)

        self.pop_up_instructions_box.setIconPixmap(instructions_image.scaled(200,200))
        self.pop_up_instructions_box.setWindowIcon(QtGui.QIcon(self.icon2_image))
        self.pop_up_instructions_box.setWindowTitle("Instructions")
        self.pop_up_instructions_box.setText(f"Welcome to {self.app_name}.\n\n"
                                             "Mass molecular weights will be calculated for the formula, adducts, and state of charge you select.\n\n"
                                             "Exact results are given within all available decimal places for each atom.\n\n"
                                             "In addition, you can add information related to compounds and copy the results obtained to your clipboard.\n\n")
        mss_box_font = self.font
        mss_box_font.setPointSize(10)
        self.pop_up_instructions_box.setFont(mss_box_font)
        self.pop_up_instructions_box.StandardButton.Ok
        self.pop_up_instructions_box.exec()

    def pop_up_about(self):
        self.pop_up_about_box = QMessageBox()

        self.pop_up_about_box.setWindowIcon(QtGui.QIcon(self.icon_image))
        self.pop_up_about_box.setWindowTitle(f"About {self.app_name}")
        self.pop_up_about_box.setText("HighResMS m/z calculator has been created as a tool for calculating molecular weights in the field of high resolution mass spectrometry (HRMS).\n\n"
                                      "Also, it can be used in any other field where it can be of help.\n\nCreated by José Raúl Belmonte. 2022.\n\nEmail: jbs324@inlumine.ual.com\n\n")
        mss_box_font = self.font
        mss_box_font.setPointSize(10)
        self.pop_up_about_box.setFont(mss_box_font)
        self.pop_up_about_box.StandardButton.Ok
        self.pop_up_about_box.exec()
