import sys
import time
import logging
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5.QtGui import QIcon
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
        self.title = 'Launch Control Client'
        self.left = 50
        self.top = 50
        self.width = 1030
        self.height = 800

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('pictures/icon.png'))
        self.setFixedSize(1030, 800)

        self.table_widget = TabManager(self)
        self.setCentralWidget(self.table_widget)

        self.MenuBar()

        self.show()

    def ToolBar(self):
        # Sets up the tool bar found right below the Menu. Has usefull applications.

        launchAction = QAction(QIcon('pictures/rocket.png'), 'Launch Window', self)
        # launchAction.triggered.connect(self.close_application)

        exitAction = QAction(QIcon('pictures/exit.png'), 'Exit', self)
        exitAction.triggered.connect(self.close_application)

        settingAction = QAction(QIcon('pictures/settings.png'), 'Settings', self)
        # settingAction.triggered.connect(self.close_application)

        connectionAction = QAction(QIcon('pictures/connection.png'), 'Connection Window', self)
        # connectionAction.triggered.connect(self.close_application)

        graphAction = QAction(QIcon('pictures/graph.png'), 'Graph Window', self)
        # graphAction.triggered.connect(self.close_application)


        self.toolBar = self.addToolBar("Launch Window")
        self.toolBar.addAction(launchAction)
        self.toolBar.addAction(graphAction)
        self.toolBar.addAction(connectionAction)
        self.toolBar.addAction(settingAction)
        self.toolBar.addAction(exitAction)

    def MenuBar(self):
        # Sets up File and About on top left of page. Most Functions are not completed yet.

        settingAction = QAction(QIcon('pictures/settings.png'), '&Settings', self)
        settingAction.setShortcut('Ctrl+S')
        settingAction.setStatusTip("Doesn't Work Right Now")
        # settingAction.triggered.connect(QtWidgets.)

        exitAction = QAction(QIcon('pictures/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close_application)

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

    def close_application(self):
        # exits GUI

        logger.debug("Application Exited at {}".format(time.asctime()))
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Client()
    sys.exit(app.exec_())