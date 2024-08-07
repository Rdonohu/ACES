

from PyQt5 import QtCore, QtGui, QtWidgets
import io
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Ui_Phone( QtWidgets.QWidget):
    ToggleAlarmSignal = QtCore.pyqtSignal(int)
    NotifyPoliceSignal = QtCore.pyqtSignal(int, name="NotifyPoliceSignal")

    def setupUi(self, Phone):
        Phone.setObjectName("Phone")
        Phone.resize(486, 743)
        self.centralwidget = QtWidgets.QWidget(Phone)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 530, 441, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.UpdateLocation = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.UpdateLocation.setObjectName("UpdateLocation")
        self.verticalLayout.addWidget(self.UpdateLocation)
        self.NotifyPolice = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.NotifyPolice.setObjectName("NotifyPolice")
        self.verticalLayout.addWidget(self.NotifyPolice)
        self.ActivateAlarm = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ActivateAlarm.setObjectName("ActivateAlarm")
        self.verticalLayout.addWidget(self.ActivateAlarm)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 491, 171))
        self.textBrowser.setObjectName("textBrowser")

        coordinate = (52.6968598,-8.9031497)
        m = folium.Map(
            title = "Current Location",
            zoom_start = 15,
            location = coordinate
        )

        folium.Marker( location = coordinate, popup="Your JLR Vehicle").add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.location = QWebEngineView(self.centralwidget)
        self.location.setHtml(data.getvalue().decode())
        self.location.setGeometry(QtCore.QRect(0, 170, 481, 361))
        self.location.setObjectName("location")
        Phone.setCentralWidget(self.centralwidget)

        self.retranslateUi(Phone)
        QtCore.QMetaObject.connectSlotsByName(Phone)

        self.UpdateLocation.clicked.connect(self.updateLocation) 
        self.NotifyPolice.clicked.connect(self.notifyPolice)
        self.ActivateAlarm.clicked.connect(self.toggleAlarm)


    def retranslateUi(self, Phone):
        _translate = QtCore.QCoreApplication.translate
        Phone.setWindowTitle(_translate("Phone", "Users Phone"))
        self.UpdateLocation.setText(_translate("Phone", "Update Location"))
        self.NotifyPolice.setText(_translate("Phone", "Notify Police"))
        self.ActivateAlarm.setText(_translate("Phone", "Activate Alarm"))
        self.textBrowser.setHtml(_translate("Phone", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:20pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#ffffff;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:16pt; color:#a31515;\">Your car has detected a break in, If this was not you please activate your desired actions below. If no Action is taken in the next 5 minutes the police will be notified with the location of the car.</span></p></body></html>"))

    def updateLocation(self):
        print("update")

    def notifyPolice(self):
        self.NotifyPoliceSignal.emit(1)
    
    def toggleAlarm(self):
        if self.ActivateAlarm.text() == "Activate Alarm":
            self.ActivateAlarm.setText("Deactivate Alarm")
            self.ToggleAlarmSignal.emit(1)
        else:
            self.ActivateAlarm.setText("Activate Alarm")
            self.ToggleAlarmSignal.emit(1)