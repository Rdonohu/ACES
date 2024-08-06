
from PyQt5 import QtCore
import time
import keyboard
import serial

class Worker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")


    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.runFlag = False
        self.speed = 0
        self.Imobiliser = False

    def startThread(self):
        if self.runFlag:
            self.runFlag = False
        elif self.runFlag == False:
            self.runFlag = True
        

    def stopThread(self):
        self.runFlag = False

    def setImobiliser(self):
        self.Imobiliser = True
    
    def unsetImobiliser(self):
        self.Imobiliser = False
    


    def run(self):
        while True:
            # demo code that increases speed on lcd when vehicle started
            #decreases speed when vehicle stopped
            while self.runFlag:
                if keyboard.is_pressed("up"):
                    if self.Imobiliser and self.speed == 0:
                        self.speed=0
                        time.sleep(0.25)
                    elif self.Imobiliser and self.speed == 15:
                        self.speed=self.speed
                        time.sleep(0.25)
                    elif self.Imobiliser and self.speed > 15:
                         self.speed=self.speed -1
                         time.sleep(0.25)
                         print("Imobiliser Engaged")
                    else:
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
    breakInFound = QtCore.pyqtSignal(bool, name="breakInFound")
    lockSignal  = QtCore.pyqtSignal(bool, name="lockSignal")
    startSignal  = QtCore.pyqtSignal(bool, name="startSignal")
    alarmSignal  = QtCore.pyqtSignal(bool, name="alarmSignal")

    def __init__(self, parent=None):
        super(ArduinoWorker, self).__init__(parent)
        self.arduino = serial.Serial(port = "COM7", timeout=0)
        time.sleep(2)
        
    def startThread(self): 
        pass
        
    def stopThread(self):
        pass

    def sendLock(self):
        self.arduino.write(str.encode("lock"))
    
    def sendUnlock(self):
        self.arduino.write(str.encode("unlock"))


    def run(self):
        while True:
            var = self.arduino.read(10)
            if var != b"":
                print(var)
                if var == b"BreakIn":
                    self.breakInFound.emit(True)
                elif var == b"ALock":
                    self.lockSignal.emit(True)
                elif var == b"Start":
                    self.startSignal.emit(True)
                elif var == b"Alarm":
                    self.alarmSignal.emit(True)
            time.sleep(0.5)


class AlarmWorker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(str, name="valueFound")

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

    def run(self):
        while True:
            if self.alarmState:
                self.valueFound.emit("background-color: red")
                time.sleep(0.5)
                self.valueFound.emit("background-color: rgb(53, 53, 53)")
                
            time.sleep(0.5)



