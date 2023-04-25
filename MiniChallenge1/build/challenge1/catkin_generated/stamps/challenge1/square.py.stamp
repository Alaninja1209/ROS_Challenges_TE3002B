#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

if __name__=='__main__':
    pub=rospy.Publisher("/cmd_vel",Twist, queue_size=10)
    rospy.init_node("path")
    wheelbase = 19.4/100 #cm to m
    wheelradius = 5/100 #cm to m
    factorLineal = 1 # 1 en gazbeo
    factorAngular= 1 # en gazebo es 1
    initialV = 0
    v = 0.5 #arduino # esto es 0.5 positivo en gazebo
    w = 0.5 #esto es 0.5 en gazebo
    vPub = Twist()
    distance = 0
    ang_distance = 0
    initialT = rospy.get_time()
    rate = rospy.Rate(10)
    
    
    timeI = rospy.get_time()
    while not rospy.is_shutdown():
        for i in range(1, 6):
            while(distance < 2):
                vPub.linear.x = v*factorLineal
                vPub.angular.z = 0
                pub.publish(vPub)
                dt = rospy.get_time() - timeI
                distance = distance + (dt * abs(v))
                timeI = rospy.get_time()
                rate.sleep()

            distance = 0
            while(ang_distance < (3.1416/2)):
                vPub.linear.x = 0
                vPub.angular.z = w*factorAngular
                pub.publish(vPub)
                dt = rospy.get_time() - timeI
                ang_distance = ang_distance + (dt * abs(w))
                timeI = rospy.get_time()
                rate.sleep()
            
            ang_distance = 0
            #rospy.loginfo("Ya acabe")
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)


        vPub.linear.x = 0
        vPub.angular.z = 0
        pub.publish(vPub)
        rospy.signal_shutdown("Over")
