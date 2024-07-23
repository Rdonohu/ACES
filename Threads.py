
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time
import keyboard

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
                if keyboard.is_pressed("up"):
                    self.speed=self.speed+1
                    time.sleep(0.25)
                    self.valueFound.emit(self.speed)
                elif self.speed > 0:
                    self.speed=self.speed-1
                    if keyboard.is_pressed("down"):
                        time.sleep(0.2)
                    else:
                        time.sleep(0.4)
                    self.valueFound.emit(self.speed)
                time.sleep(0.1)
            while not self.runFlag:
                if self.speed > 0:
                    self.speed=self.speed-1
                    time.sleep(0.5)
                    self.valueFound.emit(self.speed)
                time.sleep(0.25)


class ArduinoWorker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")

    def __init__(self, parent=None):
        super(ArduinoWorker, self).__init__(parent)
        
    def startThread(self): 
        pass
        
    def stopThread(self):
        pass

    def run(self):
        while True:
            time.sleep(0.5)
            pass


class AlarmWorker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")

    def __init__(self, console,parent=None) :
        super(AlarmWorker, self).__init__(parent)
        self.console = console
        self.alarmState = False
        
    def startAlarm(self): 
         self.alarmState = True
    
    def getState(self):
        return self.alarmState
        
    def stopAlarm(self):
        self.alarmState = False
        self.console.setStyleSheet("background-color: rgb(53, 53, 53)")

    def run(self):
        while True:
            if self.alarmState:
                # self.console.setStyleSheet("background-color: red")
                print("wee")
                time.sleep(0.5)
                # self.console.setStyleSheet("background-color: rgb(53, 53, 53)")
                print("woo")
            time.sleep(0.5)



