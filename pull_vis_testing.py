import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector

class DataModel(QObject):
    dataChanged = pyqtSignal()
    maxChanged = pyqtSignal()
    distChanged = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        # Initialize data as an array of dictionaries
        self.get_teams()
        self.get_pulls(0)
        self.pull_dist=123
        #self.max_pull=200

    @pyqtProperty(QVariant, notify=dataChanged)
    def data(self):
        return self.pull_list
    
    @pyqtProperty(int, notify=distChanged)
    def current_pull_dist(self):
        return self.pull_dist
    
    @pyqtProperty(int, notify=maxChanged)
    def max_pull_dist(self):
        return self.max_pull

    def get_teams(self):
        self.teams={}
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        localcursor=localdb.cursor()
        sql="SELECT team_id, team_name, team_abv, color FROM teams"
        localcursor.execute(sql)
        results=localcursor.fetchall()
        for i in results:
            id,name,abv,color=i
            team={"name":name,"abv":abv,"color":color}
            self.teams[id]=team

    def get_pulls(self,pull_class):
        self.pull_list=[]
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        localcursor=localdb.cursor()
        sql=f"SELECT pull_id, team_id, tractor_id, final_dist FROM all_pull_results WHERE class = {pull_class}"
        localcursor.execute(sql)
        results=localcursor.fetchall()
        dists=[]
        for x in results:
            id,team_id,tractor_id,dist =x
            pull={"id":id,"team":self.teams[team_id]["abv"],"tractor":tractor_id,"dist":dist,"color":self.teams[team_id]["color"]}
            self.pull_list.append(pull)
            dists.append(dist)
        self.max_pull=int(max(dists))
        
        

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    data_model = DataModel()

    # Expose the DataModel instance to QML
    engine.rootContext().setContextProperty("dataModel", data_model)

    engine.load(QUrl("pull_bar_testing.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
