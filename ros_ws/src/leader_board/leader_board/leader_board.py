import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import mysql.connector
import rclpy
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
from threading import *

rclpy.init()
node=rclpy.create_node('overlays')

class DataModel(QObject):
    dataChanged = pyqtSignal()
    leaderBoardChanged = pyqtSignal()
    def __init__(self):
        super().__init__()
        # Initialize data as an array of dictionaries
        print("get teams")
        self.get_teams()
        print("get tractors")
        self.get_tractors()
        self.get_leaders()
        self.current_pull=0
        self.current_pull_sub = node.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        self.leader_board_obj=[]
        self.thread()
        print("init done")

    @pyqtProperty(QVariant, notify=leaderBoardChanged)
    def leaderBoard(self):
        return self.leader_board_obj

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

    def get_tractors(self):
        self.tractors={}
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        localcursor=localdb.cursor()
        sql="SELECT tractor_id, tractor_num, tractor_name, team_id FROM tractors"
        localcursor.execute(sql)
        result = localcursor.fetchall()
        for x in result:
            tid,num,name,team_id=x
            tractor={"team_id":team_id,"name":name,"number":num}
            self.tractors[tid]=tractor


    
    def thread(self):
        t1=Thread(target=self.ros_thread)
        t1.start()

    def ros_thread(self):
        print("ros thread started")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.destroy_node()
        rclpy.shutdown()
        print("ros shutdown")

    def get_leaders(self):
        print("get leaders")
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        localcursor=localdb.cursor()
        sql="SELECT class_id, class_name FROM classes"
        localcursor.execute(sql)
        result=localcursor.fetchall()
        self.leader_board_obj=[]
        for x in result:
            pulls=[]
            class_id,class_name=x
            sql=f"SELECT tractor_id, final_dist, max_speed FROM all_pull_results WHERE class = {class_id} ORDER BY final_dist DESC LIMIT 30"
            localcursor.execute(sql)
            yresult=localcursor.fetchall()
            for y in yresult:
                tractor_id,dist,speed=y
                team_id=self.tractors[tractor_id]["team_id"]
                pull={"speed":speed,"tractor_id":tractor_id,"distance":dist,"team_id":team_id,"team_abv":self.teams[team_id]["abv"],"team_name":self.teams[team_id]["name"],"tractor_num":self.tractors[tractor_id]["number"]}
                pulls.append(pull)
            class_obj={"class_id":class_id,"class_name":class_name,"pulls":pulls}
            self.leader_board_obj.append(class_obj)
        self.leaderBoardChanged.emit()
        localdb.close()
        print(self.leader_board_obj)



    def current_pull_callback(self,msg):
        if msg.pullid!=self.current_pull:
            self.current_pull=msg.pullid
            self.get_leaders()




        
        

def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel()

    # Expose the DataModel instance to QML
    print("engine")
    engine.rootContext().setContextProperty("dataModel", data_model)
    print("load")
    engine.load(QUrl("src/leader_board/leader_board/QML/leader.qml"))
    print("engine done")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
