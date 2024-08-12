
from PyQt5 import QtCore
import time
import keyboard
import serial
import pygame 

class Worker(QtCore.QThread):
    #LCD worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")


    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.runFlag = False
        self.speed = 0
        self.Imobiliser = False
        pygame.init()
        self.car_sound = pygame.mixer.Sound("car.wav")
        self.decel_sound = pygame.mixer.Sound("decel.wav")
        self.decel_channel = pygame.mixer.Channel(3)
        self.car_channel = pygame.mixer.Channel(0)
    def play_car_sound(self):
        if not self.car_channel.get_busy():
            self.car_channel.play(self.car_sound, loops=-1)
         
    def stop_car_sound(self):
        if self.car_channel.get_busy():
            self.car_channel.stop()
    def play_decel_sound(self):
        if not self.decel_channel.get_busy():
                self.decel_channel.play(self.decel_sound, loops=-1)
    def stop_decel_sound(self):
        if self.decel_channel.get_busy():
            self.decel_channel.stop()
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
                        self.stop_decel_sound()
                        self.play_car_sound()
                           
                        time.sleep(0.25)
                    elif self.Imobiliser and self.speed > 15:
                        
                        self.speed=self.speed -1
                        self.stop_car_sound()
                        self.play_decel_sound()
                        time.sleep(0.25)
                        print("Imobiliser Engaged")
                    else:
                        self.stop_decel_sound()
                        self.play_car_sound()
                            
                        self.speed=self.speed+1
                        time.sleep(0.25)
                    self.valueFound.emit(self.speed)
                    
                elif self.speed > 0:
                    self.stop_car_sound()
                    self.play_decel_sound()
                    self.speed=self.speed-1
                    if keyboard.is_pressed("down"):
                        time.sleep(0.2)
                    else:
                        time.sleep(0.4)
                    self.valueFound.emit(self.speed)
                elif self.speed == 0:
                    self.stop_decel_sound()
                    self.stop_car_sound()
                time.sleep(0.1)
            while not self.runFlag:
                self.stop_car_sound()
                self.stop_decel_sound()
                if self.speed > 0:
                    self.speed=self.speed-1
                    time.sleep(0.5)
                    self.valueFound.emit(self.speed)
                if self.speed == 0:
                    self.stop_decel_sound()
                time.sleep(0.25)


class ArduinoWorker(QtCore.QThread):
    #arduino worker thread
    valueFound = QtCore.pyqtSignal(int, name="valueFound")
    breakInFound = QtCore.pyqtSignal(bool, name="breakInFound")
    lockSignal  = QtCore.pyqtSignal(bool, name="lockSignal")
    startSignal  = QtCore.pyqtSignal(bool, name="startSignal")
    alarmSignal  = QtCore.pyqtSignal(bool, name="alarmSignal")
    policeSignal  = QtCore.pyqtSignal(bool, name="policeSignal")
    coordsReceived = QtCore.pyqtSignal(float, float, name="coordsReceived")


    def __init__(self, parent=None):
        super(ArduinoWorker, self).__init__(parent)
        self.arduino = serial.Serial(port = "COM5", timeout=0)
        time.sleep(2)
        self.POPO_sound = pygame.mixer.Sound("police.wav")
        self.POPO_channel = pygame.mixer.Channel(2)
       
        
    def startThread(self): 
        pass
        
    def stopThread(self):
        pass

    def sendLock(self):
        self.arduino.write(str.encode("lock"))
        # pass
    def sendUnlock(self):
        self.arduino.write(str.encode("unlock"))
        # pass
    def sendPOPO(self):
        self.arduino.write(str.encode("POPO"))
        self.play_POPO_sound()
    
    def unsendPOPO(self):
        self.arduino.write(str.encode("NOP"))
        self.stop_POPO_sound()

    def play_POPO_sound(self):
        if not self.POPO_channel.get_busy():
            self.POPO_channel.play(self.POPO_sound, loops=-1)
    def stop_POPO_sound(self):
        if self.POPO_channel.get_busy():
            self.POPO_channel.stop()

    # def get_Coords(self):
    #     self.arduino.write(b'COORDS')
        
    #     buffer = ""  # Buffer to hold partial data

    #     while True:
    #         line = self.arduino.readline().decode("utf-8").strip()
            
    #         if line:
    #             buffer += line  # Accumulate the incoming data
    #             print(f"Received: {buffer}")

    #             # Look for the expected format
    #             if "LAT:" in buffer and ", LON:" in buffer:
    #                 try:
    #                     # Extract latitude and longitude from the buffer
    #                     lat_str = buffer.split('LAT:')[1].split(', LON:')[0].strip()
    #                     lon_str = buffer.split(', LON:')[1].strip()

    #                     # Convert to float
    #                     latitude = float(lat_str)
    #                     longitude = float(lon_str)

    #                     # Emit the coordinates
    #                     self.coordsReceived.emit(latitude, longitude)
                        
    #                     # Exit loop after successful parsing
    #                     return
    #                 except (IndexError, ValueError) as e:
    #                     print(f"Error parsing coordinates: {e}")
    #                     # Handle error case, possibly reset buffer
    #                     buffer = ""
    #                     return None
    #             else:
    #                 # Check if we need to handle incomplete data
    #                 if "\n" in line:  # Consider buffer reset strategy based on specific use-case
    #                     print("Incomplete data, waiting for more...")
    #         else:
    #             # Optional: Handle case when no data is received
    #             pass


    def run(self):
        x = 0
        while True:
            var = self.arduino.read(10)
            if var != b"":
                
                if var == b"BreakIn":
                    self.breakInFound.emit(True)
                elif var == b"ALock":
                    self.lockSignal.emit(True)
                elif var == b"Start":
                    self.startSignal.emit(True)
                elif var == b"Alarm":
                    self.alarmSignal.emit(True)
                elif var == b"Police":
                    self.policeSignal.emit(True)
            # if x >= 5 :
            #     self.get_Coords()
            #     x = 0
            # else:
            #     x +=1
            time.sleep(0.5)


class AlarmWorker(QtCore.QThread):
    #Alarm worker thread
    valueFound = QtCore.pyqtSignal(str, name="valueFound")
    NotifyPoliceTimer = QtCore.pyqtSignal(bool)

    def __init__(self, console,parent=None) :
        super(AlarmWorker, self).__init__(parent)
        self.console = console
        self.alarmState = False
        self.policeTimer = False
        self.Notified = False
        self.timerDuration = 10
        self.alarm_sound = pygame.mixer.Sound("alarm.wav")
        self.alarm_channel = pygame.mixer.Channel(1)
        self.get_out_sound = pygame.mixer.Sound("get_out.wav")
        self.get_out_channel = pygame.mixer.Channel(5)

    def startAlarm(self): 
        self.alarmState = True
        if not self.policeTimer:
            self.policeTimer = time.time()
        self.play_alarm_sound()
        self.play_get_out_sound()

    def getState(self):
        return self.alarmState
    def stopAlarm(self):
        self.alarmState = False
        self.policeTimer = False
        self.Notified = False
        self.stop_alarm_sound()
        
    def play_alarm_sound(self):
        if not self.alarm_channel.get_busy():
            self.alarm_channel.play(self.alarm_sound, loops=-1)
    def stop_alarm_sound(self):
        if self.alarm_channel.get_busy():
            self.alarm_channel.stop()
    def play_get_out_sound(self):
        if not self.get_out_channel.get_busy():
            self.get_out_channel.play(self.get_out_sound)

    def run(self):
        
        while True:
            if self.alarmState:
               
                self.valueFound.emit("background-color: red")
                time.sleep(0.5)
                self.valueFound.emit("background-color: rgb(53, 53, 53)")
                
                if not self.Notified:
                    if self.policeTimer != False:
                        print("start", self.policeTimer )
                        print(time.time() - self.policeTimer)
                        if time.time() - self.policeTimer >= self.timerDuration:
                            self.NotifyPoliceTimer.emit(True)
                            self.Notified = True
            time.sleep(0.5)


