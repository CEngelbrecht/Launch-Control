import sys
import time
import logging
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout, QLabel, QAction, QMenuBar, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen, QFont, QPalette
from PyQt5.QtCore import Qt
from widget_launch_control import LaunchControl


logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)



class  Start(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        # initializes the GUI with the pictures found in the pictures folder.

        palettered = QPalette()
        palettered.setColor(QPalette.Foreground, Qt.red)

        paletteblack = QPalette()
        paletteblack.setColor(QPalette.Foreground, Qt.black)

        paletteblue = QPalette()
        paletteblue.setColor(QPalette.Foreground, Qt.blue)

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

        redstripetoolbar = createPicture(self, 'red.png', 0, 65, 1200, 20)
        blackbottom = createPicture(self, 'black.png', 0, 650, 1200, 150)
        sdsulogo = createPicture(self, 'sdsu2.png', 10, 665, 100, 79)
        redlogounderline = createPicture(self, 'red2.png', 770, 695, 350, 5)
        rocketlogo = createPicture(self, 'rocket2.png', 1030, 650, 150, 150)
        whitebackground = createPicture(self, 'white.png', 0, 0, 1000, 80)
        sdsufrontpicture = createPicture(self, 'sdsu.png', 50, 150, 500, 396)

        rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 780, 650, 500, 50, 20, True, palettered)
        mainlabel = createLabel(self, 'HOME', 10, 20, 500, 50, 24, True, paletteblack)

        self.Buttons()
        self.show()



    def Buttons(self):
        # Sets up buttons found in the program

        self.font2 = QFont()
        self.font2.setPointSize(18)
        self.font3 = QFont()
        self.font3.setPointSize(12)

        connectBtn = QPushButton("Connect", self)
        connectBtn.resize(250, 100)
        connectBtn.move(613, 500)
        #connectBtn.clicked.connect()

        exitBtn = QPushButton("Exit", self)
        exitBtn.resize(250, 100)
        exitBtn.move(913, 500)
        exitBtn.clicked.connect(self.close_app)

    def paintEvent(self, e):
        # sets up the "paint brush" in order to use the drawLines function

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # draws black lines

        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        #qp.drawLine(925, 250, 625, 250)

    def color_picker(self):  # needswork

        # Not Functioning yet, used to paint GUI. (I am using pictures right now to do that)

        color.QtWidgets.QColorDialog.getColor()
        self.styleChoice.setStyleSheet("QWidget { background-color: {}".format(color.name()))

    def Time(self):  # needswork

        # going to display time on the GUI

        self.lcd.display(time.strftime("%H" + ":" + "%M"))

    def close_app(self):
        # exits GUI
        #self.logTextBox.append("> Exiting...{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
        choice = QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            pass
            #self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))
