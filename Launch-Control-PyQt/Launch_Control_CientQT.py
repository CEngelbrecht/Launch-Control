
#!/usr/bin/python3

import sys
import time
import logging
import threading
import socket 
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui, Qt


server_IP = '192.168.1.33' #This is the IP of the ESB Pi. It is a static IP. 
port = 5000
BUFF = 1024

logname=time.strftime("log/LC_ClientLog(%H_%M_%S).log",time.localtime())
logger = logging.getLogger("")                                                                 
logging.basicConfig(filename=logname, level=logging.DEBUG)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Window(QtWidgets.QMainWindow):

	def __init__(self):

		#initializes the Geometry and the overall window

		super().__init__()
		self.setGeometry(450,200,1000,700)
		self.setWindowTitle('Launch Control GUI')
		self.setWindowIcon(QtGui.QIcon('pictures/icon.png'))
		self.setFixedSize(1000,700)

		self.init_ui()

	def init_ui(self):

		#initializes the GUI with the pictures found in the pictures folder.

		backpix = QtWidgets.QLabel(self)
		backpix.setPixmap(QtGui.QPixmap('pictures/black.png'))
		backpix.move(0,575)
		backpix.resize(1000,125)

		backpix2 = QtWidgets.QLabel(self)
		backpix2.setPixmap(QtGui.QPixmap('pictures/white.png'))
		backpix2.move(0,0)
		backpix2.resize(1000,80)

		backpix3 = QtWidgets.QLabel(self)
		backpix3.setPixmap(QtGui.QPixmap('pictures/red.png'))
		backpix3.move(0,65)
		backpix3.resize(1000,20)

		pix1 = QtWidgets.QLabel(self)
		pix1.setPixmap(QtGui.QPixmap('pictures/sdsu.png'))
		pix1.move(0,-170)
		pix1.resize(1000,1000)

		pix2 = QtWidgets.QLabel(self)
		pix2.setPixmap(QtGui.QPixmap('pictures/rocketproject.png'))
		pix2.move(712,100)
		pix2.resize(150,150)

		rocketlabel = QtWidgets.QLabel(self)
		rocketlabel.setText('SDSU ROCKET PROJECT')
		rocketlabel.move(588, 200)
		rocketlabel.resize(500,50)
		rocketlabel.setFont(QtGui.QFont('Times',20,QtGui.QFont.Bold,True))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.Time)
		self.timer.start(1000)

		self.lcd = QtGui.QLCDNumber(self)
		self.lcd.display(time.strftime("%H"+":"+"%M"))

		Trying to set up a digital Clock"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		"""color = QtGui.QColor(0,0,0)

		fontColor = QtWidgets.QAction('Font bg Color', self)
		fontColor.triggered.connect(self.color_picker)

		self.toolbar.addAction(fontColor)

		Figuring out how to color"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		self.ToolBar()
		self.MenuBar()
		self.Buttons()
		#self.Time()
		self.show()

	def MenuBar(self):

		#Sets up File and About on top left of page. Most Functions are not completed yet.               
        
		settingAction = QtWidgets.QAction(QtGui.QIcon('pictures/settings.png'), '&Settings', self)
		settingAction.setShortcut('Ctrl+S')
		settingAction.setStatusTip("Doesn't Work Right Now")
		#settingAction.triggered.connect(QtWidgets.)

		exitAction = QtWidgets.QAction(QtGui.QIcon('pictures/exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(self.close_application)

		helpAction = QtWidgets.QAction(QtGui.QIcon('pictures/help.png'), '&Help', self)
		helpAction.setShortcut('Ctrl+H')
		helpAction.setStatusTip("Doesn't Wort Right Now")
		#helpAction.triggered.connect(QtWidgets.)

		aboutAction = QtWidgets.QAction(QtGui.QIcon('pictures/about.png'), '&About', self)
		aboutAction.setShortcut('Ctrl+A')
		aboutAction.setStatusTip("Doesn't Work Right Now")
		#aboutAction.triggered.connect(QtWidgets.)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		aboutMenu = menubar.addMenu('&About')
		fileMenu.addAction(settingAction)
		fileMenu.addAction(exitAction)
		aboutMenu.addAction(helpAction)
		aboutMenu.addAction(aboutAction)
        

	def Buttons(self):

		#Sets up buttons found in the program

		btn1 = QtWidgets.QPushButton("Connect", self)
		btn1.resize(150,50)
		btn1.move(613,500)
		#btn1.clicked.connect()

		btn2 = QtWidgets.QPushButton("Exit", self)
		btn2.resize(150,50)
		btn2.move(813,500)
		btn2.clicked.connect(self.close_application)

	
	def ToolBar(self):

		#Sets up the tool bar found right below the Menu. Has usefull applications.

		launchAction = QtWidgets.QAction(QtGui.QIcon('pictures/rocket.png'), 'Launch Window', self)
		#launchAction.triggered.connect(self.close_application)

		exitAction = QtWidgets.QAction(QtGui.QIcon('pictures/exit.png'), 'Exit', self)
		exitAction.triggered.connect(self.close_application)

		settingAction = QtWidgets.QAction(QtGui.QIcon('pictures/settings.png'), 'Settings', self)
		#settingAction.triggered.connect(self.close_application)

		connectionAction = QtWidgets.QAction(QtGui.QIcon('pictures/connection.png'), 'Connection Window', self)
		#connectionAction.triggered.connect(self.close_application)

		graphAction = QtWidgets.QAction(QtGui.QIcon('pictures/graph.png'), 'Graph Window', self)
		#graphAction.triggered.connect(self.close_application)


		self.toolBar = self.addToolBar("Launch Window")
		self.toolBar.addAction(launchAction)
		self.toolBar.addAction(graphAction)
		self.toolBar.addAction(connectionAction)
		self.toolBar.addAction(settingAction)
		self.toolBar.addAction(exitAction)

	def paintEvent(self, e):

                #sets up the "paint brush" in order to use the drawLines function
                
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def drawLines(self, qp):

                #draws the line seen under the sdsu logo

		pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

		qp.setPen(pen)
		qp.drawLine(925,250,625,250)

	def color_picker(self): #needswork

		#Not Functioning yet, used to paint GUI. (I am using pictures right now to do that)

		color.QtWidgets.QColorDialog.getColor()
		self.styleChoice.setStyleSheet("QWidget { background-color: {}".format(color.name()))

	def Time(self): #needswork

		#going to display time on the GUI

		self.lcd.display(time.strftime("%H"+":"+"%M"))


	def close_application(self):

		#exits GUI

		logger.debug("Application Exited at {}".format(time.asctime()))
		sys.exit()

def run():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
