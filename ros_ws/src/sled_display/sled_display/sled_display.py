import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import mysql.connector
import rclpy
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
from threading import Thread

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
    classChanged=pyqtSignal()
    chartChanged=pyqtSignal()
    timeChanged=pyqtSignal()
    
    maxForceChanged=pyqtSignal()
    maxSpeedChanged=pyqtSignal()
    powerChanged=pyqtSignal()
    maxPowerChanged=pyqtSignal()
    pullDataChanged=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.update_list()
        # Initialize data as an array of dictionaries
        print("get teams")
        self.get_teams()
        
        print("get tractors")
        self.get_tractors()
        print("get last pulls")
        self.last_pulls(1)
        print("get pulls")
        #self.get_pulls(0)
        print("get pulls done")
        self.force=0.0
        self.max_force=0.0
        self.max_speed=0.0
       
        self.pull_dist=123
        self.speed=0.0
        self.pull_durration=1.0
        self.current_class=1
        self.current_track_state=0
        self.class_name="OPEN"
        self.pull_start_time=0.0
        self.last_pulls_list=[]
        self.max_power=0.0
        self.chart_data=[{"time":0.0,"speed":0.0,"force":0.0},{"time":1.0,"speed":4,"force":2.2}]
        self.current_pull_obj={"id":0,"team":"","team_abv":"","tractor_name":"","tractor_num":0,"color":"","id":0,"max_tractor_dist":0}
        self.max_pull=200
        self.pull_list=[]
        self.pull_pub = node.create_publisher(Currentpull,'current_pull',10)
        self.sled_sub=node.create_subscription(Sled,'sled',self.sled_callback,10)
        self.current_pull_sub = node.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        self.trackstate_sub = node.create_subscription(Currentpull, 'track_state',self.track_state_callback,10)
        
        self.thread()
        print("init done")

    @pyqtProperty(QVariant, notify=pullDataChanged)
    def pullData(self):
        return self.pull_list

    @pyqtProperty(float, notify=powerChanged)
    def currentPower(self):
        return self.power
    
    @pyqtProperty(float, notify=maxPowerChanged)
    def maxPower(self):
        return self.max_power

    @pyqtProperty(QVariant, notify=chartChanged)
    def chartData(self):
        return self.chart_data

    @pyqtProperty(float, notify=maxSpeedChanged)
    def maxSpeed(self):
        return self.max_speed
    
    @pyqtProperty(float, notify=maxForceChanged)
    def maxForce(self):
        return self.max_force

    

    @pyqtProperty(float, notify=timeChanged)
    def pullDuration(self):
        return self.pull_durration
    
    @pyqtProperty(str, notify=classChanged)
    def current_class_name(self):
        return self.class_name

    @pyqtProperty(QVariant, notify=lastChanged)
    def last_pulls_qt(self):
        return self.last_pulls_list
    
    @pyqtProperty(float, notify=forceChanged)
    def pull_force(self):
        return self.force

    @pyqtProperty(QVariant, notify=dataChanged)
    def data(self):
        return self._data
    
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
            localcursor.execute("SELECT tractor_id, team_id,tractor_num, tractor_name FROM tractors where team_id="+str(team_id))
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
            #print(x)
            pull={"id":id,"team":self.teams[team_id]["abv"],"tractor":tractor_id,"dist":dist,"color":self.teams[team_id]["color"]}
            self.pull_list.append(pull)
            dists.append(dist)
        self.max_pull=int(max(dists))
        self.maxChanged.emit()
        self.pullDataChanged.emit()

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
        
    def sled_callback(self,msg):
        #print("Sled callback")
        self.pull_dist=msg.distance
        self.speed=msg.speed
        self.force=msg.force
        self.power = self.speed*1.46667*self.force/550
        if self.power>self.max_power:
            self.max_power=self.power
            self.maxPowerChanged.emit()
        time=msg.header.stamp.sec+msg.header.stamp.nanosec/1000000000
        self.pull_durration=time-self.pull_start_time
        #print(f"sec: {msg.header.stamp.sec} nano: {msg.header.stamp.nanosec} time: {time} duration: {self.pull_durration} start: {self.pull_start_time}")
        
        data={"time":self.pull_durration,"speed":self.speed,"force":self.force}
        
        
        


        if self.pull_durration-self.chart_data[-1]["time"]>.1:
            self.chart_data.append(data)
            self.chartChanged.emit()
            self.timeChanged.emit()
            
            if self.force>self.max_force:
                self.max_force=self.force
                self.maxForceChanged.emit()
            if self.speed>self.max_speed:
                self.max_speed=self.speed
                self.maxSpeedChanged.emit()
        
        
        #print(self.chart_data)
        self.powerChanged.emit()
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
            self.chart_data=[{"time":0.0,"speed":0.0,"force":0.0}]
            self.chartChanged.emit()
            #self.get_pulls(class_id)
            self.get_pulls(class_id)
            self.last_pulls(class_id)
            sql=f"SELECT class_name FROM classes WHERE class_id = {class_id}"
            localcursor.execute(sql)
            print("fetch")
            result=localcursor.fetchone()
            if type(result)!=type(None):
                ud=self.class_name!=result[0]
                self.class_name=result[0]
            
                if ud:
                    self.classChanged.emit()
            localdb.close()
    
    def last_pulls(self,class_id):
        localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
        self.last_pulls_list=[]
        localcursor=localdb.cursor()
        sql=f"SELECT team_id, tractor_id, final_dist, max_speed FROM all_pull_results WHERE class = {class_id} ORDER BY pull_id DESC LIMIT 5"
        localcursor.execute(sql)
        result=localcursor.fetchall()
        pulls=[]
        for x in result:
            team_id,tractor_id,dist,speed=x
            pull={"team_name":self.teams[team_id]["name"],"team_abv":self.teams[team_id]["abv"],"tractor_num":self.tractors[tractor_id]["number"],"distance":dist,"speed":speed}
            #pull=1
            self.last_pulls_list.append(pull)
        print(len(pulls))
        #pulls =[pulls[len(pulls)-1]]
        
        
        self.lastChanged.emit()
        localdb.close()
        print(self.last_pulls_list)




    def track_state_callback(self,msg):
        if msg.trackstate!=self.current_track_state:
            self.current_track_state=msg.trackstate
            self.trackChanged.emit()
            if self.track_state==1:
                self.pull_start_time = node.get_clock().now().nanoseconds/1000000000.0


        
        

def main():
    app = QApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel()

    # Expose the DataModel instance to QML
    print("engine")
    engine.rootContext().setContextProperty("dataModel", data_model)
    print("load")
    engine.load(QUrl("src/sled_display/sled_display/QML/live.qml"))
    print("engine done")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
