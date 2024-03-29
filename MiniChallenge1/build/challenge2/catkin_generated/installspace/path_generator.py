#!/usr/bin/env python2
import rospy
import numpy as np
import math as mt
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class pathGenerator:
    def __init__(self):
        self.wr = 0.0
        self.wl = 0.0
        self.xA = 0.0
        self.yA = 0.0
        self.theta = 0.0

        rospy.Subscriber("/wl", Float32, self.wl_callback)
        rospy.Subscriber("/wr", Float32, self.wr_callback)

        self.vPub = rospy.Publisher('/cmd_vel', Twist,  queue_size=10)
        self.rate = rospy.Rate(10)
    
    def wr_callback(self, msg):
        self.wr = msg.data

    def wl_callback(self, msg):
        self.wl = msg.data

    def pathDone(self, desPos, range):
        if (desPos[0] - range < self.xA < desPos[0] + range) and (desPos[1] - range < self.yA < desPos[1] + range):
            return True
        return False
    
    def poseController(self, desPos, desAngle):
        kt = 0.5
        kr = 0.1

        thetad = mt.atan2((desPos[1] - self.yA), (desPos[0] - self.xA))

        thetae = self.theta - thetad
        d = mt.hypot((desPos[0] - self.xA), (desPos[1] - self.yA))

        alpha_e = desAngle - self.theta
        angR = thetae + alpha_e

        v = kt *d
        omg = kr*thetae

        if omg > 3.1416/2:
            omg = 3.1416/2
        if omg < -3.1416/2:
            omg = -3.1416/2

        return v, omg

if __name__=='__main__':
    rospy.init_node('PathGenerator')
    path = pathGenerator()

    wheelBase = 0.19
    wheelRadius = 0.05

    p1 = [2, 2]
    #yd = [0, 2]
    thetad = 0.0

    current_time = rospy.get_time()
    last_time = rospy.get_time()

    msg = Twist()

    dt = 0
    prevError = 0

    while not path.pathDone(p1, 0.1):
        current_time = rospy.get_time()
        dt = current_time - last_time
        last_time = current_time

        v, omg = path.poseController(p1, 3.1416/2)

        msg.linear.x = v
        msg.angular.z = omg

        path.vPub.publish(msg)

        #Calculating velocities
        V = wheelRadius * (path.wr + path.wl)/2
        w = wheelRadius * (path.wr + path.wl)/wheelBase

        xd = V * mt.cos(path.theta)
        yd = V * mt.sin(path.theta)
        wd = w

        path.xA += xd * dt
        path.yA += yd * dt
        path.theta += wd * dt

        path.rate.sleep()

    msg.linear.x = 0.0
    path.vPub.publish(msg)
    rospy.signal_shutdown('Path completed')