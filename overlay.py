import sys
import requests
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QTimer, QUrl, QVariant, QObject,pyqtSignal, pyqtProperty
import json

app = QGuiApplication(sys.argv)
session = requests.Session()
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)


# Define a QObject to wrap the data and expose it to QML
class DataWrapper(QObject):
    dataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._dataList = []

    @pyqtProperty(QVariant,notify=dataChanged)
    def dataList(self):
        return self._dataList

    def updateData(self, data):
        self._dataList = data
        self.dataChanged.emit()

data_wrapper = DataWrapper()

def update_time():
    response = session.get('http://localhost:5000/last5')
    data_list = json.loads(response.content)
    data_wrapper.updateData(data_list)
    ##print(f"Data fetched: ",data_list)



timer = QTimer()
timer.setInterval(5000)  # 100 ms = 10 Hz
timer.timeout.connect(update_time)
timer.start()

engine.rootContext().setContextProperty("dataWrapper", data_wrapper)
engine.load(QUrl.fromLocalFile("overlay.qml"))

sys.exit(app.exec())
