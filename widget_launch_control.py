import sys
import time
import logging
import threading
import socket
import subprocess
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

server_IP = '192.168.1.33'  # This is the IP of the ESB Pi. It is a static IP.
port = 5000
BUFF = 1024

logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LaunchControl(QtWidgets.QWidget):
    def __init__(self):

        # initializes the Geometry and the overall window

        super().__init__()

        self.init_ui()

    def init_ui(self):

        # initializes the GUI with the pictures found in the pictures folder.

        palettered = QtGui.QPalette()
        palettered.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        paletteblack = QtGui.QPalette()
        paletteblack.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        paletteblue = QtGui.QPalette()
        paletteblue.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)

        # initial values
        self.kdata = "Open"
        self.mdata = "Open"
        self.ldata = "Open"
        self.bdata = "Intact"

        # time_thread = threading.Thread(target = self.get_time)
        # time_thread.start()

        # self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_address = (server_IP, port)
        self.connection_status = False  # initialzing to a false connection state
        self.arm_status = False

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):
            # makes code smaller, all the labels in the program

            slabel = QtWidgets.QLabel(self)
            slabel.setText(stext)
            slabel.move(smovex, smovey)
            slabel.resize(sresizex, sresizey)
            slabel.setFont(QtGui.QFont('Times', sfontsize, QtGui.QFont.Bold, storf))
            slabel.setPalette(scolor)

        def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):
            # makes code smaller, all the pictures in the program
            # you have to save pictures to the pictures/ path in order to show

            pix = QtWidgets.QLabel(self)
            pix.setPixmap(QtGui.QPixmap('pictures/' + spicture))
            pix.move(smovex, smovey)
            pix.resize(sresizex, sresizey)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Pictures

        # def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):

        whitetoolbar = createPicture(self, 'white.png', 0, 0, 1200, 80)
        whitebackground = createPicture(self, 'white2.png', 800, 0, 750, 700)
        redstripetoolbar = createPicture(self, 'red.png', 0, 65, 1200, 20)
        blackbottom = createPicture(self, 'black.png', 0, 650, 1200, 150)
        blacklogoback = createPicture(self, 'black2.png', 745, 85, 110, 570)
        sdsulogo = createPicture(self, 'sdsu.png', 750, 89, 100, 85)
        redlogounderline = createPicture(self, 'red2.png', 740, 695, 350, 5)
        whitebtnborder = createPicture(self, 'black3.png', 320, 180, 400, 10)
        statrborder = createPicture(self, 'rborder.png', 675, 240, 50, 400)
        statlborder = createPicture(self, 'lborder.png', 315, 240, 50, 400)
        buttonrborder = createPicture(self, 'rborder.png', 250, 240, 50, 400)
        buttonlborder = createPicture(self, 'lborder.png', 20, 240, 50, 400)
        statusboxbreak = createPicture(self, 'statusborder.png', 330, 265, 380, 48)
        statusboxmain = createPicture(self, 'statusborder.png', 330, 325, 380, 48)
        statusboxlox = createPicture(self, 'statusborder.png', 330, 385, 380, 48)
        statusboxkero = createPicture(self, 'statusborder.png', 330, 445, 380, 48)
        statusboxignitor = createPicture(self, 'statusborder.png', 330, 505, 380, 48)
        statusboxsaftey = createPicture(self, 'statusborder.png', 330, 565, 380, 48)
        rocketlogo = createPicture(self, 'rocket2.png', 1000, 650, 150, 150)
        redstripetoolbar = createPicture(self, 'red.png', 0, 650, 1200, 5)
        commandbreak = createPicture(self, 'break.png', 110, 245, 100, 10)
        statusbreak = createPicture(self, 'break.png', 470, 245, 100, 10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Labels

        # def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):

        rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 750, 650, 500, 50, 20, True, palettered)
        buttonlabel = createLabel(self, 'Commands:', 90, 190, 800, 80, 13, True, paletteblack)
        statuslabel = createLabel(self, 'Readings:', 465, 190, 800, 80, 13, True, paletteblack)
        connectionlabel = createLabel(self, 'Connection:', 985, 23, 500, 50, 9, False, paletteblue)
        connectionstatus = createLabel(self, 'Not Connected', 1080, 23, 500, 50, 9, False, paletteblue)
        breakwirelabel = createLabel(self, 'Breakwire Status', 340, 265, 500, 50, 12, False, paletteblue)
        breakwirechange = createLabel(self, 'Intact', 600, 265, 500, 50, 18, False, palettered)
        mainValvelabel = createLabel(self, 'Main Valve', 340, 325, 500, 50, 12, False, paletteblue)
        mainValvechange = createLabel(self, 'Open', 615, 325, 500, 50, 18, False, palettered)
        loxValvelabel = createLabel(self, 'Lox Valve', 340, 385, 500, 50, 12, False, paletteblue)
        loxValvechange = createLabel(self, 'Open', 615, 385, 500, 50, 18, False, palettered)
        keroValvelabel = createLabel(self, 'Kero Valve', 340, 445, 500, 50, 12, False, paletteblue)
        keroValvechange = createLabel(self, 'Open', 615, 445, 500, 50, 18, False, palettered)
        ignitorstatuslabel = createLabel(self, 'Ignitor Status', 340, 505, 500, 50, 12, False, paletteblue)
        ignitorstatuschange = createLabel(self, 'Not Lit', 590, 505, 500, 50, 18, False, palettered)
        safteystatus = createLabel(self, 'Saftey Status', 340, 565, 500, 50, 12, False, paletteblue)
        safteystatuschange = createLabel(self, 'Disarmed', 550, 565, 500, 50, 18, False, palettered)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # sets up the logging text box in the console

        self.logTextBox = QtWidgets.QTextBrowser(self)
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.logTextBox.setFont(self.font)
        self.logTextBox.setReadOnly(True)
        self.logTextBox.resize(345, 565)
        self.logTextBox.move(855, 85)
        self.logTextBox.append("========Action Log========")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.display(time.strftime("%H"+":"+"%M"))

        Trying to set up a digital Clock"""
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """color = QtGui.QColor(0,0,0)

        fontColor = QtWidgets.QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)

        self.toolbar.addAction(fontColor)

        Figuring out how to color"""
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.homeButtons()
        self.show()

    # self.Time()


    def homeButtons(self):

        # Sets up buttons found in the program

        self.font2 = QtGui.QFont()
        self.font2.setPointSize(18)
        self.font3 = QtGui.QFont()
        self.font3.setPointSize(12)

        launchBtn = QtWidgets.QPushButton("Launch!", self)
        launchBtn.resize(290, 100)
        launchBtn.move(15, 100)
        launchBtn.setFont(self.font2)
        launchBtn.clicked.connect(self.launch_app)

        igniteBtn = QtWidgets.QPushButton("Ignite!", self)
        igniteBtn.resize(210, 70)
        igniteBtn.move(310, 100)
        igniteBtn.setFont(self.font3)
        igniteBtn.clicked.connect(self.ignite_app)

        abortBtn = QtWidgets.QPushButton("Abort!", self)
        abortBtn.resize(210, 70)
        abortBtn.move(525, 100)
        abortBtn.setFont(self.font3)
        abortBtn.clicked.connect(self.abort_app)

        connectBtn = QtWidgets.QPushButton("Connect", self)
        connectBtn.resize(240, 60)
        connectBtn.move(40, 260)
        connectBtn.setFont(self.font3)
        connectBtn.clicked.connect(self.connect_app)

        open_ventsBtn = QtWidgets.QPushButton("Open Vents", self)
        open_ventsBtn.resize(240, 60)
        open_ventsBtn.move(40, 320)
        open_ventsBtn.setFont(self.font3)
        open_ventsBtn.clicked.connect(self.openvents_app)

        close_ventsBtn = QtWidgets.QPushButton("Close Vents", self)
        close_ventsBtn.resize(240, 60)
        close_ventsBtn.move(40, 380)
        close_ventsBtn.setFont(self.font3)
        close_ventsBtn.clicked.connect(self.closevents_app)

        close_mainBtn = QtWidgets.QPushButton("Close Main", self)
        close_mainBtn.resize(240, 60)
        close_mainBtn.move(40, 440)
        close_mainBtn.setFont(self.font3)
        close_mainBtn.clicked.connect(self.closemain_app)

        safteyBtn = QtWidgets.QPushButton("Toggle Saftey", self)
        safteyBtn.resize(240, 60)
        safteyBtn.move(40, 500)
        safteyBtn.setFont(self.font3)
        safteyBtn.clicked.connect(self.saftey_app)

        statusBtn = QtWidgets.QPushButton("Read Statuses", self)
        statusBtn.resize(240, 60)
        statusBtn.move(40, 560)
        statusBtn.setFont(self.font3)
        statusBtn.clicked.connect(self.status_app)

    def paintEvent(self, e):

        # sets up the "paint brush" in order to use the drawLines function

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawLines2(qp)
        qp.end()

    def drawLines(self, qp):

        # draws the red lines found in the program

        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 210, 725, 210)
        qp.drawLine(307.5, 220, 307.5, 640)

    # qp.drawLine(330,400,710,400)
    # qp.drawLine(20,205,325,205)
    # qp.drawLine(240,265,240,305)

    def drawLines2(self, qp):  # (not being used currently)

        # draws the black lines found in the program

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

    def color_picker(self):  # needswork(NotWorking)

        # Not Functioning yet, used to paint GUI. (I am using pictures right now to do that)

        color.QtWidgets.QColorDialog.getColor()
        self.styleChoice.setStyleSheet("QWidget { background-color: {}".format(color.name()))

    def Time(self):  # needswork(NotWorking)

        # going to display time on the GUI

        self.lcd.display(time.strftime("%H" + ":" + "%M"))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # This is where the functions are for the buttons and toolbar

    def launch_app(self):

        self.logTextBox.append("> Launching!{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Launching at {}".format(time.asctime()))

    def ignite_app(self):

        self.logTextBox.append("> Igniting!{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Igniting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def abort_app(self):

        self.logTextBox.append("> Aborting!{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Aborting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def connect_app(self):

        self.logTextBox.append("> Connecting...{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Connecting... at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def openvents_app(self):

        self.logTextBox.append("> Vents Opened{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Vents Opened at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def closevents_app(self):

        self.logTextBox.append("> Vents Closed{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Vents Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def closemain_app(self):

        self.logTextBox.append("> Main Closed{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Main Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def saftey_app(self):

        self.logTextBox.append("> Saftey Toggled{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Saftey Toggled at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def status_app(self):

        self.logTextBox.append("> Reading{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Reading at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def ping_app(self):

        self.logTextBox.append("Pinging Server{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        logger.debug("Pinging Server at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

    def close_app(self):
        # exits GUI
        self.logTextBox.append("> Exiting...{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        choice = QtWidgets.QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))


