import sys
import time
import logging
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout, QLabel, QAction, QMenuBar
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen, QFont
from PyQt5.QtCore import Qt


logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)



class  Start(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        # initializes the GUI with the pictures found in the pictures folder.


        backpix = QLabel(self)
        backpix.setPixmap(QPixmap('pictures/black.png'))
        backpix.move(0, 575)
        backpix.resize(1000, 125)

        backpix2 = QLabel(self)
        backpix2.setPixmap(QPixmap('pictures/white.png'))
        backpix2.move(0, 0)
        backpix2.resize(1000, 80)

        backpix3 = QLabel(self)
        backpix3.setPixmap(QPixmap('pictures/red.png'))
        backpix3.move(0, 65)
        backpix3.resize(1000, 20)

        pix1 = QLabel(self)
        pix1.setPixmap(QPixmap('pictures/sdsu.png'))
        pix1.move(0, -170)
        pix1.resize(1000, 1000)

        pix2 = QLabel(self)
        pix2.setPixmap(QPixmap('pictures/rocketproject.png'))
        pix2.move(712, 100)
        pix2.resize(150, 150)

        rocketlabel = QLabel(self)
        rocketlabel.setText('SDSU ROCKET PROJECT')
        rocketlabel.move(588, 200)
        rocketlabel.resize(500, 50)
        rocketlabel.setFont(QFont('Times', 20, QFont.Bold, True))

        self.Buttons()
        self.show()



    def Buttons(self):
        # Sets up buttons found in the program

        btn1 = QPushButton("Connect", self)
        btn1.resize(150, 50)
        btn1.move(613, 500)
        # btn1.clicked.connect()

        btn2 = QPushButton("Exit", self)
        btn2.resize(150, 50)
        btn2.move(813, 500)
        btn2.clicked.connect(self.close_application)



    def paintEvent(self, e):
        # sets up the "paint brush" in order to use the drawLines function

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # draws the line seen under the sdsu logo

        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(925, 250, 625, 250)

    def color_picker(self):  # needswork

        # Not Functioning yet, used to paint GUI. (I am using pictures right now to do that)

        color.QtWidgets.QColorDialog.getColor()
        self.styleChoice.setStyleSheet("QWidget { background-color: {}".format(color.name()))

    def Time(self):  # needswork

        # going to display time on the GUI

        self.lcd.display(time.strftime("%H" + ":" + "%M"))

    def close_application(self):
        # exits GUI

        logger.debug("Application Exited at {}".format(time.asctime()))
        sys.exit()

