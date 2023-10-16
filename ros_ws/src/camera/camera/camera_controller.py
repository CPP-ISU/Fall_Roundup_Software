#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sled_msgs.msg import Sled
from .submodules.camera_lib import camera as camera
import math
import time
import cv2 as cv
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from apriltag import Detector, DetectorOptions
from sled_msgs.msg import Currentpull

camera_position=[100,50,0]
camera_rotation=90
tractor_offset=10
zoom_max=50
zoom_min=0
dist_max=150
dist_min=50
april_target_x=500
april_target_y=500
size_target=100


cam=camera("/dev/ttyUSB0")

class MyNode(Node):

    def __init__(self):
        super().__init__('my_node')
        self.sled_sub = self.create_subscription(Sled,'sled',self.sled_callback,10)
        self.get_logger().info('My Node is running.')
        self.img_sub = self.create_subscription(Image,'camera_image',self.img_callback,10)
        self.track_state_sub = self.create_subscription(Currentpull,'track_state',self.track_state_callback,10)
        self.cv_bridge=CvBridge()
        options=DetectorOptions(quad_blur=1.0)
        self.Detector=Detector(options=options)
        self.loss_timer=self.create_timer(.25,self.loss_timer_callback)
        self.last_tag=time.time()
        self.track_state=0

    def sled_callback(self,msg):
        print("sled_callback")
        dist=msg.distance
        sled_pos=[dist,0,0]
        tractor_position=[sled_pos[0]+tractor_offset,sled_pos[1],sled_pos[2]]
        dx=tractor_position[0]-camera_position[0]
        dy=tractor_position[1]-camera_position[1]
        dz=tractor_position[2]-camera_position[2]
        tractor_cam_dist=math.sqrt(dx**2+dy**2+dz**2)
        tractor_cam_xy_dist=math.sqrt(dx**2+dy**2)
        tractor_cam_angle=[0,math.asin(dx/tractor_cam_xy_dist),math.asin(dz/tractor_cam_xy_dist)]
        tractor_cam_angle[2]=0
        print(tractor_cam_dist)
        
        zoom=max(min(zoom_min+((tractor_cam_dist-dist_min)/(dist_max-dist_min))*(zoom_max-zoom_min),16345),0)
        print(zoom)
        if time.time()-self.last_tag>=.25 and self.track_state==1:
            cam.abs_pos(18,18,math.degrees(tractor_cam_angle[1]),math.degrees(tractor_cam_angle[2]))
        #time.sleep(.1)
        #cam.zoom_pos(zoom)
    
    def track_state_callback(self,msg):
        self.track_state=msg.trackstate
        print(self.track_state)
        if self.track_state==2:
            cam.abs_pos(18,18,0,0)
        if self.track_state==3:
            cam.abs_pos(18,18,-45,0)

    def img_callback(self,msg):
        img=self.cv_bridge.imgmsg_to_cv2(msg)
        gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        try:
            detections=self.Detector.detect(gray)
        except Exception as e:
            print(f"no tag {e}")
            detections=[]
        if len(detections)>0 and self.track_state==1:
            tag_size=cv.norm(detections[0].corners[0]-detections[0].corners[1])
            x=detections[0].center[0]
            y=detections[0].center[1]
            x_offset=x-april_target_x
            y_offset=y-april_target_y
            pan=.05*x_offset
            tilt=.05*y_offset
            pan=min(max(pan,-18),18)
            tilt=min(max(tilt,-18),18)
            cam.move(int(pan),int(tilt))
            size_dif=size_target-tag_size
            cam.zoom(int(max(min(7,size_dif*.1),-7)))
            self.last_tag=time.time()


            print(f"tag x: {x} y: {y} size: {tag_size} pan: {pan} tilt: {tilt}")

    def loss_timer_callback(self):
        if time.time()-self.last_tag >+.25 and self.track_state==1:
            cam.move(0,0)
            cam.zoom(-2)
        






        
        



def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
