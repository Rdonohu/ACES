
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time

class Worker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")


    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.runFlag = False
        self.speed = 0
        

    def startThread(self):
        if self.runFlag:
            self.runFlag = False
        elif self.runFlag == False:
            self.runFlag = True
        

    def stopThread(self):
        self.runFlag = False

    def run(self):
        while True:
            # demo code that increases speed on lcd when vehicle started
            #decreases speed when vehicle stopped
            while self.runFlag:
                self.speed=self.speed+1
                time.sleep(0.5)
                self.valueFound.emit(self.speed)
            
            while not self.runFlag:
                if self.speed > 0:
                    self.speed=self.speed-1
                    time.sleep(0.5)
                    self.valueFound.emit(self.speed)
                time.sleep(0.5)