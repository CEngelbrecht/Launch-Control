import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QTextBrowser, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal


class LaunchTab(QWidget):
    def __init__(self):
        super().__init__()

        self.launch_buttons()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        title_font = QFont()
        title_font.setBold(True)
        title_font.setItalic(True)
        title_font.setPointSize(20)
        title_font.setLetterSpacing(1, 3)

        self.commands = Commands()
        self.action_log = ActionLog()
        self.launch_buttons = LaunchButtons()
        self.title_label = QLabel("Launch Control")

        self.school_logo = QLabel()
        self.school_logo.setPixmap(QPixmap("pictures/icon2.png"))
        #self.rp_pic = QPi

        self.title_label.setFont(title_font)

        grid.addWidget(self.school_logo, 0, 10, 1, 1)
        grid.addWidget(self.title_label, 0, 0, 1, 2)
        grid.addWidget(self.b_launch, 0, 2, 1 , 3)
        grid.addWidget(self.b_ignite, 0, 5, 1, 2)
        grid.addWidget(self.b_abort, 0, 7, 1, 2)
        #grid.addWidget(self.launch_buttons, 1, 0, 4, 2)
        grid.addWidget(self.commands, 5, 0, 6, 2)
        grid.addWidget(self.action_log, 1, 2, 10, 10)
        grid.addWidget(self.school_logo, 0, 10 , 1, 1)

        self.setLayout(grid)
        self.show()

    def launch_buttons(self):
        large_font = QFont()
        large_font.setPointSize(14)

        medium_font = QFont()
        medium_font.setPointSize(13)

        self.b_launch = QPushButton("Launch")
        self.b_launch.setFont(large_font)
        self.b_launch.setFixedHeight(70)

        self.b_ignite = QPushButton("Ignite")
        self.b_ignite.setFont(medium_font)
        self.b_ignite.setFixedHeight(50)

        self.b_abort = QPushButton("Abort")
        self.b_abort.setFont(medium_font)
        self.b_abort.setFixedHeight(50)




class Commands(QWidget):
    s_ping_server = pyqtSignal()
    s_open_bents = pyqtSignal()
    s_close_vents = pyqtSignal()
    s_close_main = pyqtSignal()
    s_toggle_saftey = pyqtSignal()
    s_read_statuses = pyqtSignal()

    def __init__(self):
        super().__init__()

        main_box = QVBoxLayout()

        commands_label = QLabel('Commands')

        b_ping_sever = QPushButton("Ping Server")
        b_open_vents = QPushButton("Open Vents")
        b_close_vents = QPushButton("Close Vents")
        b_close_main = QPushButton("Close Main")
        b_toggle_saftey = QPushButton("Toggle Saftey")
        b_read_statuses = QPushButton("Read Statuses")

        main_box.addWidget(commands_label)
        main_box.addWidget(b_ping_sever)
        main_box.addWidget(b_open_vents)
        main_box.addWidget(b_close_vents)
        main_box.addWidget(b_close_main)
        main_box.addWidget(b_toggle_saftey)
        main_box.addWidget(b_read_statuses)

        main_box.addStretch()

        self.setLayout(main_box)

class ActionLog(QWidget):
    def __init__(self):
        super().__init__()

        main_box = QVBoxLayout()

        action_log_label = QLabel('Action Log')
        action_log = QTextBrowser()

        main_box.addWidget(action_log_label)
        main_box.addWidget(action_log)


        self.setLayout(main_box)

class LaunchButtons(QWidget):

    def __init__(self):
        super().__init__()

        main_box = QVBoxLayout()

        large_font = QFont()
        large_font.setPointSize(14)

        medium_font = QFont()
        medium_font.setPointSize(13)

        self.b_launch = QPushButton("Launch")
        self.b_launch.setFont(large_font)
        self.b_launch.setFixedHeight(70)

        self.b_ignite = QPushButton("Ignite")
        self.b_ignite.setFont(medium_font)
        self.b_ignite.setFixedHeight(50)

        self.b_abort = QPushButton("Abort")
        self.b_abort.setFont(medium_font)
        self.b_abort.setFixedHeight(50)


        main_box.addWidget(self.b_launch)
        main_box.addWidget(self.b_ignite)
        main_box.addWidget(self.b_abort)



        #main_box.addStretch()

        self.setLayout(main_box)

