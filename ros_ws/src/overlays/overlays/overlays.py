import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector
import rclpy
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
from threading import *

rclpy.init()
node=rclpy.create_node('overlays')

class DataModel(QObject):
    dataChanged = pyqtSignal()
    maxChanged = pyqtSignal()
    distChanged = pyqtSignal()
    currentChanged = pyqtSignal()
    trackChanged=pyqtSignal()
    speedChanged=pyqtSignal()
    forceChanged=pyqtSignal()
    lastChanged=pyqtSignal()
    def __init__(self):
        super().__init__()
        # Initialize data as an array of dictionaries
        self.get_teams()
        self.get_pulls(0)
        self.get_tractors()
        self.last_pulls(1)
        print("get pulls done")
        self.force=0.0
        self.pull_dist=123
        self.speed=0.0
        self.current_class=1
        self.current_track_state=0
        self.current_pull_obj={"id":0,"team":"","team_abv":"","tractor_name":"","tractor_num":0,"color":"","id":0,"max_tractor_dist":0}
        #self.max_pull=200
        self.sled_sub=node.create_subscription(Sled,'sled',self.sled_callback,10)
        self.current_pull_sub = node.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        self.trackstate_sub = node.create_subscription(Currentpull, 'track_state',self.track_state_callback,10)
        self.thread()

    @pyqtProperty(QVariant, notify=lastChanged)
    def last_pulls_qt(self):
        return self.last_pulls_list
    
    @pyqtProperty(float, notify=forceChanged)
    def pull_force(self):
        return self.force

    @pyqtProperty(QVariant, notify=dataChanged)
    def data(self):
        return self.pull_list
    
    @pyqtProperty(float, notify=speedChanged)
    def pull_speed(self):
        return self.speed
    @pyqtProperty(int, notify=trackChanged)
    def track_state(self):
        return self.current_track_state
    @pyqtProperty(QVariant, notify=currentChanged)
    def current_pull_var(self):
        return self.current_pull_obj

    @pyqtProperty(float, notify=distChanged)
    def current_pull_dist(self):
        return self.pull_dist
    
    @pyqtProperty(int, notify=maxChanged)
    def max_pull_dist(self):
        return self.max_pull
    
    @max_pull_dist.setter
    def max_pull_dist(self, value):
        if self._max_pull != value:
            self._max_pull = value
            self.maxChanged.emit()

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
        self.dataChanged.emit()
    
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
        
    def sled_callback(self,msg):
        #print("Sled callback")
        self.pull_dist=msg.distance
        self.speed=msg.speed
        self.force=msg.force
        self.distChanged.emit()
        self.speedChanged.emit()
        self.forceChanged.emit()

    def current_pull_callback(self,msg):
        print("current pull callback")
        if msg.pullid !=self.current_pull_obj["id"]:
            pull_id=msg.pullid
            localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
            localcursor=localdb.cursor()
            sql=f"SELECT team_id, tractor_id, class FROM all_pull_results WHERE pull_id = {pull_id}"
            localcursor.execute(sql)
            result=localcursor.fetchone()
            print(result)
            team_id,tractor_id,class_id=result
            self.current_class=class_id
            sql=f"SELECT team_name, team_abv, color FROM teams WHERE team_id = {team_id}"
            localcursor.execute(sql)
            result=localcursor.fetchone()
            team_name, team_abv,color = result
            sql=f"SELECT max(final_dist) FROM all_pull_results WHERE tractor_id = {tractor_id}"
            localcursor.execute(sql)
            result = localcursor.fetchone()
            max_tractor_distance=result
            sql=f"SELECT tractor_num, tractor_name FROM tractors WHERE tractor_id = {tractor_id}"
            localcursor.execute(sql)
            result=localcursor.fetchone()
            tractor_num, tractor_name = result
            self.current_pull_obj["team"]=team_name
            self.current_pull_obj["team_abv"]=team_abv
            self.current_pull_obj["tractor_name"]=tractor_name
            self.current_pull_obj["tractor_num"]=tractor_num
            self.current_pull_obj["color"]=color
            self.current_pull_obj["max_tractor_dist"]=max_tractor_distance
            self.current_pull_obj["id"]=pull_id
            self.currentChanged.emit()
            #self.get_pulls(class_id)
            self.last_pulls(class_id)
            localdb.close()
    
    def last_pulls(self,class_id):
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        localcursor=localdb.cursor()
        sql=f"SELECT team_id, tractor_id, final_dist, max_speed FROM all_pull_results WHERE class = {class_id} ORDER BY pull_id DESC LIMIT 5"
        localcursor.execute(sql)
        result=localcursor.fetchall()
        pulls=[]
        for x in result:
            team_id,tractor_id,dist,speed=x
            pull={"team_name":self.teams[team_id]["name"],"team_abv":self.teams[team_id]["abv"],"tractor_num":self.tractors[tractor_id]["number"],"distance":dist,"speed":speed}
            pulls.append(pull)
        print(len(pulls))
        #pulls =[pulls[len(pulls)-1]]
        pulls=[]
        self.last_pulls_list=pulls
        self.lastChanged.emit()
        localdb.close()
        print(self.last_pulls_list)




    def track_state_callback(self,msg):
        if msg.trackstate!=self.current_track_state:
            self.current_track_state=msg.trackstate
            self.trackChanged.emit()


        
        

def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel()

    # Expose the DataModel instance to QML
    engine.rootContext().setContextProperty("dataModel", data_model)

    engine.load(QUrl("src/overlays/overlays/QML/Overlay.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
