import sys
import json
import time
import logging
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tabs import TabManager

#logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
#logger = logging.getLogger("")
#logging.basicConfig(filename=logname, level=logging.DEBUG)


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(325,40,1300,1000)
        self.title = 'Launch Control Client'
        self.setFixedSize(1225,950)

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/icon.png'))
        #self.setFixedSize(1030, 800)

        self.table_widget = TabManager(self)
        self.setCentralWidget(self.table_widget)

        self.client_settings = ClientSettings()
        self.client_settings.update.connect(self.update)
        self.settings_info = self.client_settings.settings

        self.MenuBar()
        self.show()

    def MenuBar(self):
        # Sets up File and About on top left of page. Most Functions are not completed yet.

        settingAction = QAction(QIcon('pictures/settings.png'), '&Settings', self)
        settingAction.setShortcut('Ctrl+S')
        settingAction.setStatusTip("Doesn't Work Right Now")
        settingAction.triggered.connect(self.client_settings.call_window)

        exitAction = QAction(QIcon('pictures/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close_app)

        helpAction = QAction(QIcon('pictures/help.png'), '&Help', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip("Doesn't Wort Right Now")
        # helpAction.triggered.connect(QtWidgets.)

        aboutAction = QAction(QIcon('pictures/about.png'), '&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip("Doesn't Work Right Now")
        # aboutAction.triggered.connect(QtWidgets.)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        aboutMenu = menubar.addMenu('&About')
        fileMenu.addAction(settingAction)
        fileMenu.addAction(exitAction)
        aboutMenu.addAction(helpAction)
        aboutMenu.addAction(aboutAction)

    def update(self, dict_signal):
        print('Applying Global Settings Change With:')
        print(dict_signal)
        self.settings = dict_signal
        self.table_widget.update(dict_signal)


    def close_app(self):
        # exits GUI
        #self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
        choice = QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            pass
            #self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))


class ClientSettings(QWidget):

    update = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.title = 'Client Settings'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 500

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/settings.png'))
        self.setFixedSize(500, 500)

        self.log_folder_label = QLabel('Log Folder:', self)
        self.log_folder_label.move(10,10)
        self.log_folder_field = QLineEdit(self)
        self.log_folder_field.move(10,30)

        self.time_folder_label = QLabel('Time:', self)
        self.time_folder_label.move(10,60)
        self.time_folder_field = QLineEdit(self)
        self.time_folder_field.move(10,80)

        self.ip_label = QLabel('Server Address:', self)
        self.ip_label.move(10,110)
        self.ip_field = QLineEdit(self)
        self.ip_field.move(10,130)

        self.port_label = QLabel('Server Port:', self)
        self.port_label.move(10,160)
        self.port_field = QLineEdit(self)
        self.port_field.move(10,180)

        self.settings_init()

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.move(420,470)
        self.apply_button.clicked.connect(self.apply_settings)

        self.apply_settings()


    def apply_settings(self):


        self.settings['countdown_time'] = int(self.time_folder_field.text())
        self.settings['ip'] = self.ip_field.text()
        self.settings['port'] = int(self.port_field.text())

        if os.path.isdir(self.log_folder_field.text()):
            self.settings['log_folder'] = self.log_folder_field.text()
            print("Log directory changes take affect after client restart")
        else :
            print('Given Log Folder Name did not exist, using old value')
            self.log_folder_field.setText(self.settings['log_folder'])

        with open('client_settings.json', 'w') as f:
            json.dump(self.settings, f)
        print('Writing to json')



        self.update.emit(self.settings)

        print('Settings Applied')

    def call_window(self):
        #This functioned is called everytime the window is opened so that
        #settings init is called to reload whatever settings are saved in config
        print('Opening Client Settings')
        self.settings_init()
        self.show()

    def settings_init(self):

        print('Opening Config')
        with open('client_settings.json', 'r') as f:
            self.settings = json.load(f)

        self.log_folder_field.setText(self.settings['log_folder'])
        self.time_folder_field.setText(str(self.settings['countdown_time']))
        self.ip_field.setText(self.settings['ip'])
        self.port_field.setText(str(self.settings['port']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Client()
    sys.exit(app.exec_())
