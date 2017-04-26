import sys
import time
import logging
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QWidget, QLabel, QLineEdit, QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon,QPixmap,QFont
from tabs import TabManager

server_IP = '192.168.1.33'  # This is the IP of the ESB Pi. It is a static IP.
port = 5000
BUFF = 1024

logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(325,90,1300,1000)
        self.title = 'Launch Control Client'
        self.setFixedSize(1225,925)

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/icon.png'))
        #self.setFixedSize(1030, 800)

        self.client_settings = ClientSettings()

        self.table_widget = TabManager(self)
        self.setCentralWidget(self.table_widget)

        self.init_UI()
        self.MenuBar()
        self.ToolBar()
        self.show()

    def init_UI(self):

        self.timert = QLabel(self)
        self.timert.setText("Countdown:")
        self.timert.move(670, 83)
        self.timert.resize(200, 50)
        self.timert.setFont(QFont('Times', 8, QFont.Bold, True))

        self.timeup = 10
        self.timert = QLabel(self)
        self.timert.setText("10")
        self.timert.move(820, 92)
        self.timert.resize(100, 50)
        self.timert.setFont(QFont('Times', 20, QFont.Bold, False))


        def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):
            # makes code smaller, all the labels in the program

            slabel = QLabel(self)
            slabel.setText(stext)
            slabel.move(smovex, smovey)
            slabel.resize(sresizex, sresizey)
            slabel.setFont(QFont('Times', sfontsize, QFont.Bold, storf))
            slabel.setPalette(scolor)

        def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):
            # makes code smaller, all the pictures in the program
            # you have to save pictures to the pictures/ path in order to show

            pix = QLabel(self)
            pix.setPixmap(QPixmap('pictures/' + spicture))
            pix.move(smovex, smovey)
            pix.resize(sresizex, sresizey)

        whitetoolbar = createPicture(self, 'white3.png', 0, 0, 1300, 80)
        timerbackground = createPicture(self, 'timerback.png', 635, 100, 300, 39)

        timeBtn = QPushButton("Start", self)
        timeBtn.move(668, 115)
        timeBtn.resize(125, 20)
        timeBtn.clicked.connect(self.timer1)

    def ToolBar(self):
        # Sets up the tool bar found right below the Menu. Has usefull applications.

        homeAction = QAction(QIcon('pictures/home.png'), 'Home', self)
        #homeAction.triggered.connect(self.close_application)

        launchAction = QAction(QIcon('pictures/rocket.png'), 'Launch Control', self)
        # launchAction.triggered.connect(self.close_application)

        exitAction = QAction(QIcon('pictures/exit.png'), 'Exit', self)
        exitAction.triggered.connect(self.close_app)

        settingAction = QAction(QIcon('pictures/settings.png'), 'Settings', self)
        settingAction.triggered.connect(self.client_settings.show)

        connectionAction = QAction(QIcon('pictures/connection.png'), 'Connections', self)
        # connectionAction.triggered.connect(self.close_application)

        graphAction = QAction(QIcon('pictures/graph.png'), 'Graphs', self)
        # graphAction.triggered.connect(self.close_application)


        self.toolBar = self.addToolBar("Launch Window")
        self.toolBar.addAction(homeAction)
        self.toolBar.addAction(launchAction)
        self.toolBar.addAction(graphAction)
        self.toolBar.addAction(connectionAction)
        self.toolBar.addAction(settingAction)
        self.toolBar.addAction(exitAction)

    def timer0(self):
        if self.timeup > 0:
            self.timeup -= 1
            self.timert.setText(str(self.timeup))

    def timer1(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer0)
        self.timer.start(1000)

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


        self.settings_init()

    def call_window(self):
        #This functioned is called everytime the window is opened so that
        #settings init is called to reload whatever settings are saved in config
        self.settings_init()
        self.show()

    def settings_init(self):
        #Unfinished
        #Would load current setting from config
        self.log_folder_field.setText('log')
        self.time_folder_field.setText(str(10))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Client()
    sys.exit(app.exec_())