
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

		palettered = QtGui.QPalette()
		palettered.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)

		paletteblack = QtGui.QPalette()
		paletteblack.setColor(QtGui.QPalette.Foreground,QtCore.Qt.black)

		paletteblue = QtGui.QPalette()
		paletteblue.setColor(QtGui.QPalette.Foreground,QtCore.Qt.blue)

		#initial values
		self.kdata = "Open"
		self.mdata = "Open"
		self.ldata = "Open"
		self.bdata = "Intact"

		#time_thread = threading.Thread(target = self.get_time)
		#time_thread.start()

		#self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server_address = (server_IP,port)
		self.connection_status = False #initialzing to a false connection state
		self.arm_status = False

		def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf,scolor):

			#makes code smaller, all the labels in the program

			slabel = QtWidgets.QLabel(self)
			slabel.setText(stext)
			slabel.move(smovex, smovey)
			slabel.resize(sresizex, sresizey)
			slabel.setFont(QtGui.QFont('Times',sfontsize,QtGui.QFont.Bold,storf))
			slabel.setPalette(scolor)

		def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):

			#makes code smaller, all the pictures in the program
			#you have to save pictures to the pictures/ path in order to show

			pix = QtWidgets.QLabel(self)
			pix.setPixmap(QtGui.QPixmap('pictures/'+spicture))
			pix.move(smovex,smovey)
			pix.resize(sresizex,sresizey)

		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
								#Pictures

		sdsulogo = createPicture(self, 'sdsu.png', 0, -170, 1000, 1000)
		whitetoolbar = createPicture(self, 'white.png', 0, 0, 1000, 80)
		redstripetoolbar = createPicture(self, 'red.png', 0, 65, 1000, 20)
		blackbottom = createPicture(self, 'black.png', 0, 575, 1000, 125)
		redlogounderline = createPicture(self, 'red2.png', 560, 625, 350, 5)
		buttonborder = createPicture(self, 'border.png', 606, 190, 165, 370)
		statsborder = createPicture(self, 'border.png', 810, 190, 165, 370)
		statusboxbreak = createPicture(self, 'statusborder.png', 832, 274, 120, 28)
		statusboxmain = createPicture(self, 'statusborder.png', 832, 326, 120, 28)
		statusboxlox = createPicture(self, 'statusborder.png', 832, 376, 120, 28)
		statusboxkero = createPicture(self, 'statusborder.png', 832, 426, 120, 28)
		statusboxignitor = createPicture(self, 'statusborder.png', 832, 474, 120, 28)
		statusboxsaftey = createPicture(self, 'statusborder.png', 832, 521, 120, 28)
		rocketlogo = createPicture(self, 'rocket2.png', 825, 580, 150, 150)

		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
								#Labels

		rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 570, 580, 500, 50, 20, True, palettered)
		buttonlabel = createLabel(self, 'Commands:', 645, 160, 500, 50, 9, True, paletteblack)
		statuslabel = createLabel(self, 'Readings', 854, 160, 500, 50, 9, True, paletteblack)
		connectionlabel = createLabel(self, 'Connection:', 787, 27, 500, 50, 9, False, paletteblue)
		connectionstatus = createLabel(self, 'Not Connected', 880, 27, 500, 50, 9, False, paletteblue)
		breakwirelabel = createLabel(self, 'Breakwire Status', 827, 240, 500, 50, 9, False, paletteblue)
		breakwirechange = createLabel(self, 'Intact', 857, 263, 500, 50, 14, False, palettered)
		mainValvelabel = createLabel(self, 'Main Valve', 850, 290, 500, 50, 9, False, paletteblue)
		mainValvechange = createLabel(self, 'Open', 860, 313, 500, 50, 14, False, palettered)
		loxValvelabel = createLabel(self, 'Lox Valve', 854, 340, 500, 50, 9, False, paletteblue)
		loxValvechange = createLabel(self, 'Open', 860, 363, 500, 50, 14, False, palettered)
		keroValvelabel = createLabel(self, 'Kero Valve', 851, 390, 500, 50, 9, False, paletteblue)
		keroValvechange = createLabel(self, 'Open', 860, 413, 500, 50, 14, False, palettered)
		ignitorstatuslabel = createLabel(self, 'Ignitor Status', 840, 439, 500, 50, 9, False, paletteblue)
		ignitorstatuschange = createLabel(self, 'Not Lit', 852, 463, 500, 50, 14, False, palettered)
		safteystatus = createLabel(self, 'Saftey Status', 842, 486, 500, 50, 9, False, paletteblue)
		safteystatuschange = createLabel(self, 'Disarmed', 837, 510, 500, 50, 14, False, palettered)


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
		self.homeButtons()
		self.show()
		#self.Time()


	def homeButtons(self):

		#Sets up buttons found in the program

		btn1 = QtWidgets.QPushButton("Launch!", self)
		btn1.resize(180, 60)
		btn1.move(595,100)
		#btn4.clicked.connect(self.close_application)

		btn2 = QtWidgets.QPushButton("Ignite!", self)
		btn2.resize(180, 60)
		btn2.move(800,100)
		#btn4.clicked.connect(self.close_application)

		btn3 = QtWidgets.QPushButton("Abort!", self)
		btn3.resize(150, 50)
		btn3.move(614,200)
		#btn4.clicked.connect(self.close_application)

		btn4 = QtWidgets.QPushButton("Connect", self)
		btn4.resize(150,50)
		btn4.move(614,260)
		#btn1.clicked.connect()

		btn5 = QtWidgets.QPushButton("Open Vents", self)
		btn5.resize(150,50)
		btn5.move(614,320)
		#btn4.clicked.connect(self.close_application)

		btn6 = QtWidgets.QPushButton("Close Vents", self)
		btn6.resize(150,50)
		btn6.move(614,380)
		#btn4.clicked.connect(self.close_application)

		btn7 = QtWidgets.QPushButton("Close Main", self)
		btn7.resize(150,50)
		btn7.move(614,440)
		#btn3.clicked.connect(self.close_application)

		btn8 = QtWidgets.QPushButton("Toggle Saftey", self)
		btn8.resize(150,50)
		btn8.move(614,500)
		#btn2.clicked.connect(self.close_application)

		btn9 = QtWidgets.QPushButton("Read Statuses", self)
		btn9.resize(150, 50)
		btn9.move(818,200)
		#btn4.clicked.connect(self.close_application)



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

	
	def ToolBar(self):

		#Sets up the tool bar found right below the Menu. Has usefull applications.

		homeAction = QtWidgets.QAction(QtGui.QIcon('pictures/home.png'), 'Home Window(NotWorking)', self)
		#homeAction.triggered.connect(self.close_application)

		launchAction = QtWidgets.QAction(QtGui.QIcon('pictures/rocket.png'), 'Launch Window(NotWorking)', self)
		#launchAction.triggered.connect(self.close_application)

		exitAction = QtWidgets.QAction(QtGui.QIcon('pictures/exit.png'), 'Exit', self)
		exitAction.triggered.connect(self.close_application)

		settingAction = QtWidgets.QAction(QtGui.QIcon('pictures/settings.png'), 'Settings', self)
		#settingAction.triggered.connect(self.close_application)

		connectionAction = QtWidgets.QAction(QtGui.QIcon('pictures/connection.png'), 'Ping Server', self)
		#connectionAction.triggered.connect(self.close_application)

		graphAction = QtWidgets.QAction(QtGui.QIcon('pictures/graph.png'), 'Graph Window(NotWorking)', self)
		#graphAction.triggered.connect(self.close_application)


		self.toolBar = self.addToolBar("Launch Window")
		self.toolBar.addAction(homeAction)
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
		self.drawLines2(qp)
		qp.end()

	def drawLines(self, qp):

	    #draws the red lines found in the program

		pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		qp.drawLine(625,170,945,170)
		qp.drawLine(790,190,790,550)

	def drawLines2(self, qp): #(not being used currently)

	    #draws the black lines found in the program

		pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)



	def color_picker(self): #needswork(NotWorking)

		#Not Functioning yet, used to paint GUI. (I am using pictures right now to do that)

		color.QtWidgets.QColorDialog.getColor()
		self.styleChoice.setStyleSheet("QWidget { background-color: {}".format(color.name()))

	def Time(self): #needswork(NotWorking)

		#going to display time on the GUI

		self.lcd.display(time.strftime("%H"+":"+"%M"))



	def close_application(self):

		#exits GUI

		logger.debug("Application Exited at {}".format(time.asctime()))
		sys.exit()

class Tabs(QtWidgets.QMainWindow):#(NotWorking)

	#Tabs, they do not work currently, putting them in a different class to keep them from activating

    def __init__(self):

        #initializes the Geometry and the overall window

        super().__init__()
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget() 
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        self.tab4 = QtWidgets.QWidget()

        self.tabs.setGeometry(450,200,1000,700)
        self.tabs.setWindowTitle('Launch Control GUI')
        self.tabs.setWindowIcon(QtGui.QIcon('pictures/icon.png'))
        self.tabs.setFixedSize(1000,700)

        self.tabs.addTab(QtWidgets.QWidget(),'Tab 1')
        self.tabs.addTab(QtWidgets.QWidget(),'Tab 2')
        self.tabs.addTab(QtWidgets.QWidget(),'Tab 3')

        self.tabs.show()

def run():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
