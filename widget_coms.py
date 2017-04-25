import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QTextBrowser


class Communication(QWidget):
    def __init__(self):
        super().__init__()

        #self.serial_feed = None
        #self.coms_status = None

        self.initUI()


        self.serial_feed.append('No connection')
        self.serial_feed.append('Test')


    def initUI(self):
        serial_feed_label = QLabel('Serial Feed')
        coms_status_label = QLabel('Status')

        self.serial_feed = QTextBrowser()
        self.coms_status = QTextBrowser()



        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(serial_feed_label, 1, 0)
        grid.addWidget(self.serial_feed, 1, 1, 20, 1)


        grid.addWidget(coms_status_label, 22, 0)
        grid.addWidget(self.coms_status, 22, 1)


        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()