#!/usr/bin/env python2
import rospy
from geometry_msgs.msg import Twist

if __name__=='__main__':
    pub=rospy.Publisher("/cmd_vel",Twist, queue_size=10)
    rospy.init_node("path")
    wheelbase = 19.4/100 #cm to m
    wheelradius = 5/100 #cm to m
    factorLineal = 1
    factorAngular= 30
    initialV = 0
    v = 0.5 
    w = 0.5 
    vPub = Twist()
    distance = 0
    ang_distance = 0
    initialT = rospy.get_time()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        timeI = rospy.get_time()
        for i in range(1, 4):

            while(distance < 2):
                rospy.loginfo("Empieza")
                vPub.linear.x = v*factorLineal
                vPub.angular.z = 0
                pub.publish(vPub)
                dt = rospy.get_time() - timeI
                distance = distance + (dt * v)
                rospy.loginfo(dt)
                timeI = rospy.get_time()
                rate.sleep()

            distance = 0
            while(ang_distance < (3.1416/2)):
                vPub.linear.x = 0
                vPub.angular.z = w*factorAngular
                pub.publish(vPub)
                dt = rospy.get_time() - timeI
                ang_distance = ang_distance + (dt * w)
                rospy.loginfo(dt)
                timeI = rospy.get_time()
                rate.sleep()
        
            ang_distance = 0
        #rospy.loginfo("Ya acabe")
        vPub.linear.x = 0
        pub.publish(vPub)
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        #pub.publish(hello_str)
