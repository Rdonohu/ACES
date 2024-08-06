from PyQt5 import QtCore, QtGui, QtWidgets
from Threads import Worker, ArduinoWorker, AlarmWorker

class Ui_MainWindow(object):
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
        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
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
        self.AlarmTest.setGeometry(QtCore.QRect(30, 280, 161, 81))
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        # end of GUI Set up ---------------------------------------------------------------------------------------------------------------------------------------
        #Connecting slots i.e functions that occur when button is clicked------------------------------------------------------------------------------------------
        self.StartButton.clicked.connect(self.StartVehicle) 
        self.VehicleLock.clicked.connect(self.LockVehicle)
        self.AlarmTest.clicked.connect(self.ToggleAlarm)
        self.ActivateImobiliser.clicked.connect(self.ActivateImobiliserMode)
        self.PoliceNotifier.clicked.connect(NotifyPolice)
        self.OwnerNotifier.clicked.connect(NotifyOwner)
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
        self.ArduinoWorker.start()

        self.AlarmWorker = AlarmWorker(self.graphicsView)
        self.AlarmWorker.valueFound.connect(self.AlarmOnValueFound)
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
        self.OwnerNotifier.setText(_translate("MainWindow", "Notify Owner"))
    
    # when speedo thread send back a value this function is used
    def OnValueFound(self, value):
        self.Speedometer.display(value)

    def StartVehicle(self):
        # this function is called when start button is pressed
        #toggle between start and stop button states
        if self.StartButton.text()  == "start vehicle":
            self.StartButton.setText("Stop Vehicle")
            self.StartButton.setStyleSheet("background-color : red;")
            if self.VehicleLock.text()  == "Locked":
                if not self.AlarmWorker.getState():
                    self.AlarmWorker.startAlarm()
                    self.worker.setImobiliser()

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
            if self.AlarmWorker.getState():
                self.AlarmWorker.stopAlarm()
                self.worker.unsetImobiliser()
        else:
            #Lock vehicle
            self.VehicleLock.setText("Locked")
            self.ArduinoWorker.sendLock()
            self.VehicleLock.setStyleSheet("background-color : red;")

    def ToggleAlarm(self):
        # this function is called when button is pressed
        if self.AlarmWorker.getState():
            self.AlarmWorker.stopAlarm()
            self.ActivateImobiliserMode()
        else:
            self.AlarmWorker.startAlarm()
            self.ActivateImobiliserMode()

    def ActivateImobiliserMode(self):
        # this function is called when button is pressed
        if self.worker.Imobiliser:
            self.worker.unsetImobiliser()
        else:
            self.worker.setImobiliser()
    
    def BreakInFound(self):
        if self.VehicleLock.text()  == "Locked":
            self.AlarmWorker.startAlarm()
            self.ActivateImobiliserMode()
    

def NotifyPolice():
    # this function is called when button is pressed
    print("police are on the way")

def NotifyOwner():
    # this function is called when button is pressed
    print("The owner has been notified")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
