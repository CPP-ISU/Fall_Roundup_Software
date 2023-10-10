import sys
from PyQt5.QtCore import Qt, QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="darkcyde15",
  database='pulls'
)

mycursor = mydb.cursor()

class DataModel(QObject):
    def __init__(self):
        super().__init__()
        self.update_list()
        #print(self._data)
        

    @pyqtProperty("QVariantList")
    def data(self):
        print("pulling data")
        return self._data

    @data.setter
    def data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    @pyqtSlot()
    def update_list(self):
        localdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="darkcyde15",
        database='pulls'
        )
        localcursor = localdb.cursor()
        localcursor.execute("SELECT * FROM teams")
        myresult = localcursor.fetchall()
        self._data = []

        for result in myresult:
            tractors=[]
            team_id,team_name,team_abrev=result
            localcursor.execute("SELECT * FROM tractors where team_id="+str(team_id))
            tractor_result=localcursor.fetchall()
            for i in tractor_result:
                pulls=[]
                tractor_id,team_id,tractor_num=i
                localcursor.execute("SELECT pull_id, final_dist FROM all_pull_results where tractor_id="+str(tractor_id))
                pullresult = localcursor.fetchall()
                for j,x in enumerate(pullresult):
                    pull_id,dist=x
                    pull={"pull_id":pull_id,"dist":dist,"hook_num":j+1}
                    pulls.append(pull)
                pull={"pull_id":0,"dist":0,"hook_num":len(pullresult)+1}
                pulls.append(pull)
                
                tractor={"tractor_id":tractor_id,"team_id":team_id,"tractor_num":tractor_num,"pulls":pulls}
                tractors.append(tractor)

            out={"team_id":team_id,"team_name":team_name,"team_abrev":team_abrev,"tractors":tractors}
            self._data.append(out)
        self.dataChanged.emit()


    @pyqtSlot(list)
    def start_pull(self,data):
        print(f"pull started {data}")

    dataChanged = pyqtSignal()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    # Create a DataModel instance to hold the array data
    data_model = DataModel()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("dataModel", data_model)
    

    # Load the QML file
    engine.load("display_qml/sled_display.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

