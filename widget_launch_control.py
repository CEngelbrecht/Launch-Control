import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QTextBrowser, QPushButton, QHBoxLayout


class LaunchControl(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        launch_button = QPushButton("Launch Me", self)

        hbox = QHBoxLayout()
        hbox.addWidget(launch_button)

