import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sled_msgs.msg import Sled
import math
import time
import cv2 as cv
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


camera_position=[100,50,0]
camera_rotation=90
tractor_offset=10
zoom_max=50
zoom_min=0
dist_max=150
dist_min=50

cap=cv.VideoCapture(6)



class MyNode(Node):

    def __init__(self):
        super().__init__('my_node')
        self.img_pub = self.create_publisher(Image,"camera_image",10)
        self.timer=self.create_timer(.01,self.timer_callback)
        self.get_logger().info('My Node is running.')
        self.cv_bridge=CvBridge()

    def timer_callback(self):
        ret, img=cap.read()
        if ret:
            ros_img=self.cv_bridge.cv2_to_imgmsg(img,encoding='bgr8')
            self.img_pub.publish(ros_img)

        



        
        



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
