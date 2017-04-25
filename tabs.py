from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from widget_start import StartWidget
from widget_launch_control import LaunchControl
from widget_coms import Communication


class TabManager(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        #Init Tabs
        self.launch_control = LaunchControl()
        self.communication = Communication()
        self.start_page = StartWidget(self)
        #self.tab_name = customWidget()

        #Connect Tabs
        self.tabs.addTab(self.start_page, "Start")
        self.tabs.addTab(self.launch_control, "Launch Control")
        self.tabs.addTab(self.communication, "Communication")

        #Add tabs to widget
        self.communication.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.communication.layout.addWidget(self.pushButton1)
        self.communication.setLayout(self.communication.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
            print("\n")
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())