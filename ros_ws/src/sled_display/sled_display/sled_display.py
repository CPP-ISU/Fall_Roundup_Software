import sys
from PyQt5.QtCore import Qt, QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector
import rclpy
from sled_msgs.msg import Currentpull


mydb = mysql.connector.connect(
  host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
  user="admin",
  password="darkcyde15",
  database='fallrounudp'
)

mycursor = mydb.cursor()
rclpy.init()
node=rclpy.create_node('sled_display')

class DataModel(QObject):
    def __init__(self):
        super().__init__()
        self.update_list()
        #print(self._data)
        self.pull_pub = node.create_publisher(Currentpull,'current_pull',10)
        

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
        host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="darkcyde15",
        database='fallrounudp'
        )
        localcursor = localdb.cursor()
        localcursor.execute("SELECT team_id, team_name, team_abv FROM teams")
        myresult = localcursor.fetchall()
        self._data = []

        for result in myresult:
            tractors=[]
            team_id,team_name,team_abrev=result
            localcursor.execute("SELECT tractor_id, team_id,tractor_num FROM tractors where team_id="+str(team_id))
            tractor_result=localcursor.fetchall()
            for i in tractor_result:
                pulls=[]
                tractor_id,team_id,tractor_num,tractor_name=i
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
        localdb = mysql.connector.connect(
        host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="darkcyde15",
        database='fallrounudp'
        )
        localcursor = localdb.cursor()
        print(f"pull started {data}")
        pull=Currentpull()
        if data[3]==0:
            sql="INSERT INTO all_pull_results (class, team_id, tractor_id) VALUES (%s, %s, %s)"
            values=(data[0], data[1], data[2])
            localcursor.execute(sql,values)
            localdb.commit()
            localcursor.execute("SELECT max(pull_id) FROM all_pull_results")
            x=localcursor.fetchone()
            print(x[0])
            pull.pullid=int(x[0])
        else:
            pull.pullid=data[3]
        self.pull_pub.publish(pull)

            
        

    dataChanged = pyqtSignal()

def main():
    app = QGuiApplication(sys.argv)
    
    # Create a DataModel instance to hold the array data
    data_model = DataModel()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("dataModel", data_model)
    

    # Load the QML file
    engine.load("src/sled_display/sled_display/QML/sled_display.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

