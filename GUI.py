# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


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
        self.ActivateLimp = QtWidgets.QPushButton(self.frame_2)
        self.ActivateLimp.setGeometry(QtCore.QRect(30, 180, 161, 81))
        self.ActivateLimp.setObjectName("ActivateLimp")
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
        self.ActivateLimp.clicked.connect(ActivateLimpMode)
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
        self.worker.valueFound.connect(self.ArduinoOnValueFound)
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
        self.ActivateLimp.setText(_translate("MainWindow", "Activate Limp Mode"))
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
        # when alarm thread sends back a value this function is used to interpret the value sent back
    def AlarmOnValueFound(self,value ):
        self.graphicsView.setStyleSheet(value)
        self.Speedometer.setStyleSheet(value)


    def LockVehicle(self):
        # this function is called when button is pressed
        if self.VehicleLock.text()  == "Locked":
            #unlock vehicle
            self.VehicleLock.setText("Lock")
            self.VehicleLock.setStyleSheet("background-color : rgb(0, 181, 87)")
            print("unLockVehicle")
        else:
            #Lock vehicle
            self.VehicleLock.setText("Locked")
            self.VehicleLock.setStyleSheet("background-color : red;")
            print("LockVehicle")

    def ToggleAlarm(self):
        # this function is called when button is pressed
        if self.AlarmWorker.getState():
            self.AlarmWorker.stopAlarm()
        else:
            self.AlarmWorker.startAlarm()

def NotifyPolice():
    # this function is called when button is pressed
    print("police are on the way")

def NotifyOwner():
    # this function is called when button is pressed
    print("The owner has been notified")

def ActivateLimpMode():
    # this function is called when button is pressed
    print(" limp")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
