from PyQt5 import QtCore, QtGui, QtWidgets
from Threads import Worker, ArduinoWorker, AlarmWorker
from phone import Ui_Phone

# TODO: implement slider for key distance
class Ui_MainWindow(QtWidgets.QWidget):
    ToOwnerToggleAlarmSignal = QtCore.pyqtSignal(bool)
    PoliceNotifiedSignal  = QtCore.pyqtSignal(bool)
    def setupUi(self, MainWindow):
        

        # GUI Set Up DONT MIND THIS PART -----------------------------------------------------------------------------------------------------------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1335, 915)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 20, 1011, 721))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.StartButton = QtWidgets.QPushButton(self.frame)
        self.StartButton.setGeometry(QtCore.QRect(70, 600, 61, 41))
        self.StartButton.setMouseTracking(False)
        self.StartButton.setStyleSheet("background-color : rgb(0, 181, 87)")
        self.StartButton.setObjectName("StartButton")
        self.VehicleLock = QtWidgets.QPushButton(self.frame)
        self.VehicleLock.setGeometry(QtCore.QRect(790, 560, 101, 91))
        self.VehicleLock.setStyleSheet("background-color : rgb(0, 181, 87)")
        self.VehicleLock.setObjectName("VehicleLock")
        self.Speedometer = QtWidgets.QLCDNumber(self.frame)
        self.Speedometer.setEnabled(True)
        self.Speedometer.setGeometry(QtCore.QRect(370, 280, 230, 65))
        self.Speedometer.setStyleSheet("background-color: rgb(53, 53, 53)")
        self.Speedometer.setObjectName("Speedometer")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(-10, 80, 1001, 621))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("range-rover-05.jpg"))
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QTextBrowser(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(10, 330, 271, 161))
        self.graphicsView.setStyleSheet("background-color: rgb(53, 53, 53)")
        self.graphicsView.setObjectName("graphicsView")
        self.label.raise_()
        self.StartButton.raise_()
        self.VehicleLock.raise_()
        self.Speedometer.raise_()
        self.graphicsView.raise_()
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(1040, 90, 211, 381))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.AlarmTest = QtWidgets.QPushButton(self.frame_2)
        self.AlarmTest.setGeometry(QtCore.QRect(30, 270, 161, 81))
        self.AlarmTest.setObjectName("AlarmTest")
        self.ActivateImobiliser = QtWidgets.QPushButton(self.frame_2)
        self.ActivateImobiliser.setGeometry(QtCore.QRect(30, 180, 161, 81))
        self.ActivateImobiliser.setObjectName("ActivateImobiliser")
        self.PoliceNotifier = QtWidgets.QPushButton(self.frame_2)
        self.PoliceNotifier.setGeometry(QtCore.QRect(30, 90, 161, 81))
        self.PoliceNotifier.setObjectName("PoliceNotifier")
        self.OwnerNotifier = QtWidgets.QPushButton(self.frame_2)
        self.OwnerNotifier.setGeometry(QtCore.QRect(30, 0, 161, 81))
        self.OwnerNotifier.setObjectName("OwnerNotifier")
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(200, 800, 500, 40))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(500)
        # self.slider.setValue(0)
        self.slider.setTickPosition( QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(50)
        self.slider.setObjectName("Slider")
        self.slider.setTracking(False)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
       
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 750, 150, 50))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        # end of GUI Set up ---------------------------------------------------------------------------------------------------------------------------------------
        #Connecting slots i.e functions that occur when button is clicked------------------------------------------------------------------------------------------
        self.StartButton.clicked.connect(self.StartVehicle) 
        self.VehicleLock.clicked.connect(self.LockVehicle)
        self.AlarmTest.clicked.connect(self.ToggleAlarm)
        self.ActivateImobiliser.clicked.connect(self.ActivateImobiliserMode)
        self.PoliceNotifier.clicked.connect(self.NotifyPolice)
        self.OwnerNotifier.clicked.connect(self.NotifyOwner)
        self.slider.valueChanged.connect(self.distanceFromKey)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # -----------------------------------------------------------------------------------------------------------------------------------------------------------

        #create threads for different functionalities ---------------------------------------------------------------------------------------------------------------
        self.worker = Worker()
        #connect thread signal to slot
        self.worker.valueFound.connect(self.OnValueFound)
        #start thread
        self.worker.start()

        self.ArduinoWorker = ArduinoWorker()
        self.ArduinoWorker.valueFound.connect(self.ArduinoOnValueFound)
        self.ArduinoWorker.breakInFound.connect(self.BreakInFound)
        self.ArduinoWorker.lockSignal.connect(self.LockVehicle)
        self.ArduinoWorker.startSignal.connect(self.StartVehicle)
        self.ArduinoWorker.alarmSignal.connect(self.ToggleAlarm)
        self.ArduinoWorker.policeSignal.connect(self.NotifyPolice)
        self.ArduinoWorker.start()

        self.AlarmWorker = AlarmWorker(self.graphicsView)
        self.AlarmWorker.valueFound.connect(self.AlarmOnValueFound)
        self.AlarmWorker.NotifyPoliceTimer.connect(self.policeTimer)
        self.AlarmWorker.start()
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    def retranslateUi(self, MainWindow):
        # dont bother with this
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "start vehicle"))
        self.VehicleLock.setText(_translate("MainWindow", "lock"))
        self.AlarmTest.setText(_translate("MainWindow", "toggle alarm"))
        self.ActivateImobiliser.setText(_translate("MainWindow", "Activate Imobiliser Mode"))
        self.PoliceNotifier.setText(_translate("MainWindow", "Notify Police"))
        self.OwnerNotifier.setText(_translate("MainWindow", "Open Owner App"))
        self.label.setText(_translate("MainWindow", "Distance from car to key"))
        
    
    # when speedo thread send back a value this function is used
    def OnValueFound(self, value):
        self.Speedometer.display(value)

    def StartVehicle(self):
        # this function is called when start button is pressed
        #toggle between start and stop button states
        if self.StartButton.text()  == "start vehicle":
            self.StartButton.setText("Stop Vehicle")
            self.StartButton.setStyleSheet("background-color : red;")
            self.BreakInFound()
                    

        else:
            self.StartButton.setText("start vehicle")
            self.StartButton.setStyleSheet("background-color : rgb(0, 181, 87)")
        # send signal to thread
        # starts speed to thread
        self.worker.startThread()
    

    def ArduinoOnValueFound(self):
        # when arduino thread sends back a value this function is used to interpret the value sent back
        #send signal to arduino
        self.ArduinoWorker.startThread()

    def AlarmOnValueFound(self,value ):
        # when alarm thread sends back a value this function is used to interpret the value sent back
        self.graphicsView.setStyleSheet(value)
        self.Speedometer.setStyleSheet(value)


    def LockVehicle(self):
        # this function is called when button is pressed
        if self.VehicleLock.text()  == "Locked":
            #unlock vehicle
            self.VehicleLock.setText("Lock")
            self.VehicleLock.setStyleSheet("background-color : rgb(0, 181, 87)")
            self.ArduinoWorker.sendUnlock()
            self.ArduinoWorker.unsendPOPO()
            # if self.AlarmWorker.getState():
            #     self.AlarmWorker.stopAlarm()
            #     self.worker.unsetImobiliser()
            
                
        else:
            #Lock vehicle
            self.VehicleLock.setText("Locked")
            self.ArduinoWorker.sendLock()
            self.VehicleLock.setStyleSheet("background-color : red;")

    def ToggleAlarm(self):
        # this function is called when button is pressed
        print(self.AlarmWorker.getState())
        if self.AlarmWorker.getState():
            self.AlarmWorker.stopAlarm()
            self.worker.unsetImobiliser()
            self.ToOwnerToggleAlarmSignal.emit(False)
            self.graphicsView.setHtml("")
            self.ArduinoWorker.unsendPOPO()
        else:
            self.AlarmWorker.startAlarm()
            self.worker.setImobiliser()
            try:
                if not self.ui_phone.isVisible():
                    self.Phone.show()
                    self.ToOwnerToggleAlarmSignal.emit(True)
                    
            except:
                self.NotifyOwner()
                self.ui_phone.alarmTriggeredNotification()
            self.ToOwnerToggleAlarmSignal.emit(True)
            self.graphicsView.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#343535;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:16pt; color:white;\">THE OWNER HAS BEEN NOTIFIED WITH THE LIVE LOCATION OF THIS VEHICLE</span></p></body></html>")

    def ActivateImobiliserMode(self):
        # this function is called when button is pressed
        if self.worker.Imobiliser:
            self.worker.unsetImobiliser()
        else:
            self.worker.setImobiliser()
    
    def BreakInFound(self):
        if self.VehicleLock.text()  == "Locked":
            self.AlarmWorker.startAlarm()
            self.worker.setImobiliser()
            try:
                if not self.ui_phone.isVisible():
                    self.Phone.show()
                    self.ui_phone.alarmTriggeredNotification()
                    self.ToOwnerToggleAlarmSignal.emit(True)
                    
            except:
                self.NotifyOwner()
                self.ui_phone.alarmTriggeredNotification()
            self.ToOwnerToggleAlarmSignal.emit(True)
            self.graphicsView.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#343535;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:16pt; color:white;\">THE OWNER HAS BEEN NOTIFIED WITH THE LIVE LOCATION OF THIS VEHICLE</span></p></body></html>")


    def NotifyOwner(self):
    # this function is called when button is pressed
        self.Phone = QtWidgets.QMainWindow()
        self.ui_phone = Ui_Phone()
        self.ui_phone.setupUi(self.Phone)
        self.ui_phone.ToggleAlarmSignal.connect(self.ToggleAlarm)
        self.ui_phone.NotifyPoliceSignal.connect(self.NotifyPolice)
        self.ToOwnerToggleAlarmSignal.connect(self.ui_phone.updateAlarmButton)
        self.PoliceNotifiedSignal.connect(self.ui_phone.policeNotifiedNotification)
        if self.AlarmWorker.getState():
            self.ToOwnerToggleAlarmSignal.emit(True)
        else:
            self.ToOwnerToggleAlarmSignal.emit(False)
        self.Phone.show()


    def NotifyPolice(self):
        # this function is called when button is pressed
        self.graphicsView.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#343535;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:16pt; color:white;\">THE OWNER AND LAW ENFORCEMENT HAVE BEEN NOTIFIED WITH THE LIVE LOCATION OF THIS VEHICLE</span></p></body></html>")
        self.AlarmWorker.startAlarm()
        self.worker.setImobiliser()
        self.ToOwnerToggleAlarmSignal.emit(True)
        self.ArduinoWorker.sendPOPO()
        self.PoliceNotifiedSignal.emit(True)

    def distanceFromKey(self, value):
        pass
    
    def policeTimer(self):
        self.NotifyPolice()
        




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
