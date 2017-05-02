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

# Get a Timer Reset button. Also Maybe link the abort button to the countdown timer.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LaunchControl(QtWidgets.QWidget):
    def __init__(self):

        # initializes the Geometry and the overall window

        super().__init__()
        self.server_address = (server_IP,port)
        self.connection_status = False
        self.infotimer = QtCore.QTimer()

        self.init_ui()

    def init_ui(self):

        # initializes the GUI with the pictures found in the pictures folder.

        self.palettered = QtGui.QPalette()
        self.palettered.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        self.paletteblack = QtGui.QPalette()
        self.paletteblack.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        self.paletteblue = QtGui.QPalette()
        self.paletteblue.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)

        # initial values
        self.kdata = "Open"
        self.mdata = "Open"
        self.ldata = "Open"
        self.bdata = "Intact"

        # time_thread = threading.Thread(target = self.get_time)
        # time_thread.start()

        self.server_address = (server_IP, port)
        self.connection_status = False  # initialzing to a false connection state
        self.arm_status = False

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        #grid.addWidget(self.serial_feed, tl_vertical_grid_pos, tl_hor_grid_pos, vertical_grid_length_min, hor_grid_width_min

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

        #All of the Pictures that change states.

        self.statusbreakred = QtWidgets.QLabel(self)
        self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusbreakred.move(500, 265)
        self.statusbreakred.resize(380, 48)

        self.statusmainred = QtWidgets.QLabel(self)
        self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusmainred.move(500, 325)
        self.statusmainred.resize(380, 48)

        self.statusbloxred = QtWidgets.QLabel(self)
        self.statusbloxred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusbloxred.move(500, 385)
        self.statusbloxred.resize(380, 48)

        self.statuskerored = QtWidgets.QLabel(self)
        self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statuskerored.move(500, 445)
        self.statuskerored.resize(380, 48)

        self.statusignitorred = QtWidgets.QLabel(self)
        self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusignitorred.move(500, 505)
        self.statusignitorred.resize(380, 48)

        self.statussafteyred = QtWidgets.QLabel(self)
        self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statussafteyred.move(500, 565)
        self.statussafteyred.resize(380, 48)

        # def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):

        whitetoolbar = createPicture(self, 'white.png', 0, 0, 1200, 80)
        whitebackground = createPicture(self, 'white2.png', 800, 0, 750, 700)
        redstripetoolbar = createPicture(self, 'red.png', 0, 65, 1200, 20)
        blackbottom = createPicture(self, 'black.png', 0, 650, 1200, 150)
        blacklogoback = createPicture(self, 'black2.png', 745, 85, 60, 570)
        sdsulogo = createPicture(self, 'sdsu2.png', 10, 665, 100, 79)
        redlogounderline = createPicture(self, 'red2.png', 770, 695, 350, 5)
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
        rocketlogo = createPicture(self, 'rocket2.png', 1030, 650, 150, 150)
        redstripetoolbar = createPicture(self, 'red.png', 0, 650, 1200, 5)
        commandbreak = createPicture(self, 'break.png', 110, 245, 100, 10)
        statusbreak = createPicture(self, 'break.png', 470, 245, 100, 10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Labels

        # def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):

        self.mainlabel = createLabel(self, 'LAUNCH CONTROL', 10, 20, 500, 50, 24, True, self.paletteblack)
        self.rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 780, 650, 500, 50, 20, True, self.palettered)
        self.buttonlabel = createLabel(self, 'Commands:', 90, 190, 800, 80, 13, True, self.paletteblack)
        self.statuslabel = createLabel(self, 'Readings:', 465, 190, 800, 80, 13, True, self.paletteblack)
        self.connectionlabel = createLabel(self, 'Connection:', 985, 23, 500, 50, 9, False, self.paletteblue)
        self.breakwirelabel = createLabel(self, 'Breakwire Status', 340, 265, 500, 50, 12, False, self.paletteblue)
        self.mainValvelabel = createLabel(self, 'Main Propellant Valve', 338, 325, 500, 50, 10, False, self.paletteblue)
        self.loxValvelabel = createLabel(self, 'Lox Vent Valve', 340, 385, 500, 50, 12, False, self.paletteblue)
        self.keroValvelabel = createLabel(self, 'Kero Vent Valve', 340, 445, 500, 50, 12, False, self.paletteblue)
        self.ignitorstatuslabel = createLabel(self, 'Ignitor Status', 340, 505, 500, 50, 12, False, self.paletteblue)
        self.safteystatus = createLabel(self, 'Saftey Status', 340, 565, 500, 50, 12, False, self.paletteblue)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # All of the labels that change states.

        self.connectionstatus = QtWidgets.QLabel(self)
        self.connectionstatus.setText('Not Connected')
        self.connectionstatus.move(1080, 23)
        self.connectionstatus.resize(500, 50)
        self.connectionstatus.setFont(QtGui.QFont('Times', 9, QtGui.QFont.Bold, False))
        self.connectionstatus.setPalette(self.paletteblue)

        self.breakwirechange = QtWidgets.QLabel(self)
        self.breakwirechange.setText('Intact')
        self.breakwirechange.move(600, 265)
        self.breakwirechange.resize(500, 50)
        self.breakwirechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.breakwirechange.setPalette(self.paletteblack)

        self.mainValvechange = QtWidgets.QLabel(self)
        self.mainValvechange.setText('Open')
        self.mainValvechange.move(615, 325)
        self.mainValvechange.resize(500, 50)
        self.mainValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.mainValvechange.setPalette(self.paletteblack)

        self.loxValvechange = QtWidgets.QLabel(self)
        self.loxValvechange.setText('Closed')
        self.loxValvechange.move(615, 385)
        self.loxValvechange.resize(500, 50)
        self.loxValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.loxValvechange.setPalette(self.paletteblack)

        self.keroValvechange = QtWidgets.QLabel(self)
        self.keroValvechange.setText('Open')
        self.keroValvechange.move(615, 445)
        self.keroValvechange.resize(500, 50)
        self.keroValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.keroValvechange.setPalette(self.paletteblack)

        self.ignitorstatuschange = QtWidgets.QLabel(self)
        self.ignitorstatuschange.setText('Not Lit')
        self.ignitorstatuschange.move(590, 505)
        self.ignitorstatuschange.resize(500, 50)
        self.ignitorstatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.ignitorstatuschange.setPalette(self.paletteblack)

        self.safteystatuschange = QtWidgets.QLabel(self)
        self.safteystatuschange.setText('Disarmed')
        self.safteystatuschange.move(550, 565)
        self.safteystatuschange.resize(500, 50)
        self.safteystatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.safteystatuschange.setPalette(self.paletteblack)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # sets up the logging text box in the console

        self.logTextBox = QtWidgets.QTextBrowser(self)
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.logTextBox.setFont(self.font)
        self.logTextBox.setReadOnly(True)
        self.logTextBox.resize(400, 565)
        self.logTextBox.move(800, 85)
        self.logTextBox.append("  =========Action Log=========")

        timerbackground = createPicture(self, 'timerback.png', 635, 0, 300, 39)

        self.timert = QtWidgets.QLabel(self)
        self.timert.setText("Countdown: ")
        self.timert.move(670, -18)
        self.timert.resize(200, 50)
        self.timert.setFont(QtGui.QFont('Times', 8, QtGui.QFont.Bold, True))

        self.timeup = -60
        self.timert = QtWidgets.QLabel(self)
        self.timert.setText("-60")
        self.timert.move(845, -10)
        self.timert.resize(100, 50)
        self.timert.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold, False))

        self.timerT = QtWidgets.QLabel(self)
        self.timerT.setText("T")
        self.timerT.move(800, -10)
        self.timerT.resize(100, 50)
        self.timerT.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold, False))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """color = QtGui.QColor(0,0,0)

        fontColor = QtWidgets.QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)

        self.toolbar.addAction(fontColor)

        Figuring out how to color"""
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.setLayout(grid)
        self.homeButtons()
        self.show()

    # self.Time()


    def homeButtons(self):

        # Sets up buttons found in the program

        self.font2 = QtGui.QFont()
        self.font2.setPointSize(18)
        self.font3 = QtGui.QFont()
        self.font3.setPointSize(12)

        self.launchBtn = QtWidgets.QPushButton("Launch!", self)
        self.launchBtn.resize(290, 100)
        self.launchBtn.move(15, 100)
        self.launchBtn.setEnabled(False)
        self.launchBtn.setFont(self.font2)
        self.launchBtn.clicked.connect(self.launch_app)

        self.igniteBtn = QtWidgets.QPushButton("Ignite!", self)
        self.igniteBtn.resize(210, 70)
        self.igniteBtn.move(310, 100)
        self.igniteBtn.setEnabled(False)
        self.igniteBtn.setFont(self.font3)
        self.igniteBtn.clicked.connect(self.ignite_app)

        self.abortBtn = QtWidgets.QPushButton("Abort!", self)
        self.abortBtn.resize(210, 70)
        self.abortBtn.move(525, 100)
        self.abortBtn.setEnabled(False)
        self.abortBtn.setFont(self.font3)
        self.abortBtn.clicked.connect(self.abort_app)

        self.ping_serverBtn = QtWidgets.QPushButton("Connect", self)
        self.ping_serverBtn.resize(240, 60)
        self.ping_serverBtn.move(40, 260)
        self.ping_serverBtn.setFont(self.font3)
        self.ping_serverBtn.clicked.connect(self.connect_app)

        self.open_ventsBtn = QtWidgets.QPushButton("Open Vents", self)
        self.open_ventsBtn.resize(240, 60)
        self.open_ventsBtn.move(40, 320)
        self.open_ventsBtn.setFont(self.font3)
        self.open_ventsBtn.clicked.connect(self.openvents_app)

        self.close_ventsBtn = QtWidgets.QPushButton("Close Vents", self)
        self.close_ventsBtn.resize(240, 60)
        self.close_ventsBtn.move(40, 380)
        self.close_ventsBtn.setFont(self.font3)
        self.close_ventsBtn.clicked.connect(self.closevents_app)

        self.close_mainBtn = QtWidgets.QPushButton("Close Main", self)
        self.close_mainBtn.resize(240, 60)
        self.close_mainBtn.move(40, 440)
        self.close_mainBtn.setFont(self.font3)
        self.close_mainBtn.clicked.connect(self.closemain_app)

        self.safteyBtn = QtWidgets.QPushButton("Toggle Saftey", self)
        self.safteyBtn.resize(240, 60)
        self.safteyBtn.move(40, 500)
        self.safteyBtn.setFont(self.font3)
        self.safteyBtn.clicked.connect(self.saftey_app)

        self.statusBtn = QtWidgets.QPushButton("Read Statuses", self)
        self.statusBtn.resize(240, 60)
        self.statusBtn.move(40, 560)
        self.statusBtn.setFont(self.font3)
        self.statusBtn.clicked.connect(self.get_info)

        self.timeBtn = QtWidgets.QPushButton("Start", self)
        self.timeBtn.move(668, 15)
        self.timeBtn.resize(125, 20)
        self.timeBtn.setEnabled(False)
        self.timeBtn.clicked.connect(self.timer1)

        self.pingBtn = QtWidgets.QPushButton("Ping Server", self)
        self.pingBtn.move(1070, 20)
        self.pingBtn.resize(125, 20)
        self.pingBtn.clicked.connect(self.ping_app)

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

    def timer0(self):
        self.timeup += 1
        self.timert.setText(str(self.timeup))
        if self.timeup >= 1:
            self.timerT.setText("T+")

    def timer1(self):
        self.logTextBox.append("  >  Timer Started!{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer0)
        self.timer.start(1000)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # This is where the functions are for the buttons and toolbar

    def launch_app(self):

        self.logTextBox.append("  >  Launching!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Launching at {}".format(time.asctime()))
        self.send_info('L')

    def break_status(self):

        self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statgreen'))

    def lox_status(self):

        self.statusbloxred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))

    def kero_status(self):

        self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))

    def ignite_app(self):

        self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
        self.logTextBox.append("  >  Igniting!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Igniting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
        self.send_info('Ig')

    def abort_app(self):

        self.logTextBox.append("  >  Aborting!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Aborting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
        self.send_info('A')

    def connect_app(self):

        self.logTextBox.append("  >  Connecting...{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))

        try:
            self.s = socket.create_connection(self.server_address,timeout = 1.5)
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'Socket Successfully Bound.\nClick "Read Statuses " to start')
            self.connection_status = True
            self.connectionstatus.setText('Connected')
            self.logTextBox.append("  >  Connected{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Connection Successful at {}".format(time.asctime()))

            #self.infotimer = QtCore.QTimer()
            self.infotimer.timeout.connect(self.get_info)
            self.infotimer.setInterval(200)
            self.infotimer.start()
            self.logTextBox.append(" > Starting Get Info Timer{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Started Get Info Timer at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

        except socket.error as e:
            logger.debug("Connection Unsuccessful at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            reply = QtWidgets.QMessageBox.critical(self, "Connection Results", "Couldn't connect to {} at {}. Error is: \n{}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1],e),
                                                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)
            if reply == QtWidgets.QMessageBox.Cancel:
                self.logTextBox.append("  >  Connection Canceled{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
            elif reply == QtWidgets.QMessageBox.Retry:
                self.connect_app()


    def openvents_app(self):

        self.logTextBox.append("  >  Vents Opened{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Vents Opened at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
        self.send_info('VO')

    def closevents_app(self):

        self.logTextBox.append("  >  Vents Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Vents Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
        self.send_info('VC')

    def closemain_app(self):

        self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
        self.logTextBox.append("  >  Main Propellant Valve Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        logger.debug("Main Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
        self.send_info('MC')

    def saftey_app(self):

        if self.connection_status == True:
            if self.arm_status == False:
                self.igniteBtn.setEnabled(True)
                self.launchBtn.setEnabled(True)
                self.abortBtn.setEnabled(True)
                self.timeBtn.setEnabled(True)
                self.safteystatuschange.setText('Armed')
                self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.logTextBox.append("  >  Saftey Toggled{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
                self.arm_status = True

            elif self.arm_status == True:
                self.igniteBtn.setEnabled(False)
                self.launchBtn.setEnabled(False)
                self.abortBtn.setEnabled(False)
                self.timeBtn.setEnabled(False)
                self.safteystatuschange.setText('Disarmed')
                self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.logTextBox.append("  >  Saftey Toggled{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
                self.arm_status = False

        elif self.connection_status == False:
            logger.debug("Connection Error, Safety will not toggle unless client is connected to server at {}".format(time.asctime()))
            reply = QtWidgets.QMessageBox.critical(self, 'Connection Error', 'Safety will not toggle unless client is connected to server',
                                                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)
            if reply == QtWidgets.QMessageBox.Cancel:
                self.logTextBox.append("  >  Saftey Canceled{}".format(time.strftime("       -\t(%H:%M:%S)", time.localtime())))
            elif reply == QtWidgets.QMessageBox.Retry:
                self.saftey_app()

    def ping_app(self):

        QtWidgets.QMessageBox.information(self, '', 'Pinging...')
        #response = subprocess.call(["ping", server_IP,"-c1", "-W1","-q"])
        response = subprocess.call("ping {} -n 1 -w 1".format(server_IP)) #This is Windows syntax.
        logger.debug("Pinging Server at {}".format(time.asctime()))
        self.logTextBox.append("  >  Pinging Server{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))

        if response == 0:
            QtWidgets.QMessageBox.information(self, 'Ping Results', 'Ping to {} sucessful!\nGo ahead and connect.'.format(server_IP))
            logger.debug("Ping_Sucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Successful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
        else:
            QtWidgets.QMessageBox.information(self, 'Ping Results', "Ping to {} unsucessful!\nCheck the IP you're connecting to, or if server is online.".format(server_IP))
            logger.debug("Ping_Unsucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Unsucessful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))

    def send_info(self,command):

        if command == 'MO':
            message = b'main_open'
            logger.debug("main_open at {}".format(time.asctime()))
        elif command == 'MC':
            message = b'main_close'
            logger.debug("main_close at {}".format(time.asctime()))
        elif command == 'VO':
            message = b'vents_open'
            logger.debug("vents_open at {}".format(time.asctime()))
        elif command == 'VC':
            message = b'vents_close'
            logger.debug("vents_close at {}".format(time.asctime()))
        elif command == 'L':
            message = b'launch'
            logger.debug("launch at {}".format(time.asctime()))
        elif command == 'A':
            message = b'abort'
            logger.debug("abort at {}".format(time.asctime()))
        elif command == "Ig":
            message = b"ign1_on"
            logger.debug("ign1_on at {}".format(time.asctime()))

        self.s.send(message)
        data = self.s.recv(BUFF)
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if data == 'Ignitor 1 Lit':
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statgreen.png')) #Check if he wants green
            self.ignitorstatuschange.setText('Lit af')
            logging.info("Ignitor 1 lit: {}".format(time_now))
            logger.debug("Ignitor_1_lit at {}".format(time.asctime()))
        elif data == 'Ignitor 1 Off':
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            self.ignitorstatuschange.setText('Not Lit')
            logger.debug("Ignitor_1_Off at {}".format(time.asctime()))

    def switch_label(self,label):

        #These statements change the status of the labels
        if label == 'bwire':
            if self.breakwirechange.text() == 'Intact':
                self.breakwirechange.setText('Broken')
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                logger.debug("bwire_Broken at {}".format(time.asctime()))
            elif self.breakwirechange.text() == 'Broken':
                self.breakwirechange.setText('Intact')
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                logger.debug("bwire_Intact at {}".format(time.asctime()))

        if label == 'main':
            if self.mainValvechange.text() == 'Open':
                self.mainValvechange.setText('Closed')
                self.mainValvechange.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                logger.debug("main_Closed at {}".format(time.asctime()))
            elif self.mainValvechange.text() == 'Closed':
                self.mainValvechange.setText('Open')
                self.mainValvechange.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                logger.debug("main_Open at {}".format(time.asctime()))

        if label == 'kero':
            if self.keroValvechange.text() == 'Open':
                self.keroValvechange.setText('CloseFd')
                self.keroValvechange.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                logger.debug("kero_Closed at {}".format(time.asctime()))
            elif self.keroValvechange.text() == 'Open':
                self.keroValvechange.setText('Open')
                self.keroValvechange.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                logger.debug("kero_Open at {}".format(time.asctime()))

        if label == 'lox':
            if self.loxValvechange.text() == 'Open':
                self.loxValvechange.setText('Closed')
                self.loxValvechange.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                logger.debug("lox_Closed at {}".format(time.asctime()))
            elif self.loxValvechange.text() == 'Closed':
                self.loxValvechange.setText('Open')
                self.loxValvechange.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                logger.debug("lox_Open at {}".format(time.asctime()))

    def get_info(self):
        
        #self.logTextBox.append("  >  Reading{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
        #logger.debug("Reading at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

        try:
            self.s.send(b'bwire_status')
            self.bdata = self.s.recv(BUFF)

            self.s.send(b'main_status')
            self.mdata = self.s.recv(BUFF)

            self.s.send(b'kero_status')
            self.kdata = self.s.recv(BUFF)

            self.s.send(b'LOX_status')
            self.ldata = self.s.recv(BUFF)

        except (socket.error,AttributeError) as err:
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            logging.error("{},{}".format(time_now,err))
            logger.debug("{},{}".format(time_now,err))

        #The following if statements call the label to be changed only if the server sends a message that contradicts the current status of the label 
        if self.bdata.decode("utf-8") != self.breakwirechange.text():
            self.switch_label("bwire")
            print("Break Wire Changed:")
            print(self.bdata)
            logger.debug("bwire_status of {} at {}".format(str(self.bdata),time.asctime()))

        if self.mdata.decode("utf-8") != self.mainValvechange.text():
            self.switch_label('main')
            print("Main Changed:")
            print(self.mdata)
            logger.debug("main_status of {} at {}".format(str(self.mdata),time.asctime()))

        if self.kdata.decode("utf-8") != self.keroValvechange.text():
            self.switch_label('kero')
            print("Kero Changed:")
            print(self.kdata)
            logger.debug("kero_status of {} at {}".format(str(self.kdata),time.asctime()))

        if self.ldata.decode("utf-8") != self.loxValvechange.text():
            self.switch_label('lox')
            print("Lox Changed:")
            print(str(self.ldata))
            logger.debug("lox_status of {} at {}".format(str(self.ldata),time.asctime()))



    def close_app(self):
        # exits GUI
        self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
        choice = QtWidgets.QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?", 
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))

