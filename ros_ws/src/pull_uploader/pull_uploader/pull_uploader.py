import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
from rclpy.serialization import serialize_message
import time
import csv
import mysql.connector

class YourNode(Node):
    def __init__(self):
        super().__init__('your_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.track_sub=self.create_subscription(Currentpull, 'track_state',self.trackstate_callback,10)
        self.track_state=0
        self.timer = self.create_timer(1,self.timer_callback)
        self.update_list()
        print(self.pull_list)


    def current_pull_callback(self,msg):
        print("current pull callback")
        self.current_pullid=msg.pullid
    
    def trackstate_callback(self,msg):
        self.track_state=msg.trackstate
    
    def timer_callback(self):
        if self.track_state!=1:
            self.update_list()
            localdb = mysql.connector.connect(
            host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
            user="admin",
            password="darkcyde15",
            database='fallrounudp'
            )
            localcursor = localdb.cursor()
            for key in self.pull_list:
                if self.pull_list[key]!=1:
                    try:
                        with open(f"{key}") as file:
                            print("opening file")
                            reader=csv.reader(file)
                            data=[]
                            speed=[]
                            dist=[]
                            for row in reader:
                                speed.append(float(row[1]))
                                dist.append(float(row[0]))
                                data.append((float(row[0]),float(row[1]),float(row[2]),key))
                                #data.append(row)
                                #sql="INSERT INTO pull_data (distance, speed, draft_force) VALUES (%s, %s, %s)"
                                #localcursor.execute(sql,(float(row[0]),float(row[1]),float(row[2])))
                            sql="INSERT INTO pull_data (distance, speed, draft_force, pull_id) VALUES (%s, %s, %s, %s)"
                            localcursor.executemany(sql,data)
                            sql=f"UPDATE all_pull_results SET uploaded = 1 WHERE(pull_id ={key})"
                            localcursor.execute(sql)
                            if len(speed)>1:
                                sql=f"UPDATE all_pull_results SET max_speed = {max(speed)} WHERE(pull_id ={key})"
                                localcursor.execute(sql)
                                sql=f"UPDATE all_pull_results SET final_dist = {max(dist)} WHERE(pull_id ={key})"
                                localcursor.execute(sql)
                            localdb.commit()
                            print("upload complete")
                            
                    except Exception as e:
                        print(f"error {e}")
            localdb.close()
                    
                    



    def update_list(self):
        self.pull_list={}
        localdb = mysql.connector.connect(
        host="iqs-fallroundup.cvjcxenhbni5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="darkcyde15",
        database='fallrounudp'
        )
        localcursor = localdb.cursor()
        localcursor.execute("SELECT pull_id, uploaded FROM all_pull_results")
        myresult = localcursor.fetchall()
        for x in myresult:
            id, uploaded=x
            self.pull_list[id]=uploaded
        localdb.close()



            






def main(args=None):
    rclpy.init(args=args)
    node = YourNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()