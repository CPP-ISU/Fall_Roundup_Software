import sys
from PyQt5.QtCore import Qt, QObject, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

class ChartData(QObject):
    def __init__(self):
        super().__init__()
        self._data = []

    @pyqtProperty(list)
    def data(self):
        return self._data

    def update_data(self, new_data):
        self._data = new_data

def main():
    app = QApplication(sys.argv)
    
    engine = QQmlApplicationEngine()

    chart_data = ChartData()
    context = engine.rootContext()
    context.setContextProperty("chartData", chart_data)

    engine.load("chart_example.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
