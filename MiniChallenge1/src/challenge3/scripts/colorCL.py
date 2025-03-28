#!/usr/bin/env python
import rospy
import math as mt
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_msgs.msg import String

#Declared variables of ros suscriber
wR = 0.0
wL = 0.0
color = " "

def wr_callback(data):
    global wR
    wR = data.data

def wl_callback(data):
    global wL
    wL = data.data

def color_callback(data):
    global color
    color = data.data

if __name__=='__main__':
    sub = rospy.Subscriber("/color", String, color_callback)

    #Define robot parameters
    wheelRadius = 0.05
    wheelBase = 0.19
    dt = 0.01
    t = 0

    vMax = 0
    wMax = 3.1416/2

    #Initial robot states
    x = 0
    y = 0
    theta = 0

    #Desired positions
    xd = [2, 3.5]
    yd = [0, 0]
    kpr = 1.5
    kpt = 4.5

    rospy.init_node('PathGenerator')
    rate = rospy.Rate(100)

    pV = Twist() #Puzzlebot Velocities
    vMax = 0.35
    i = 0

    vPub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    wlSub = rospy.Subscriber('/wl', Float32, wl_callback)
    wrSub = rospy.Subscriber('/wr', Float32, wr_callback)

    while not rospy.is_shutdown():
        for i in range(len(xd)):
            d = 1
            while (d > 0.1):
                thetad = mt.atan2((yd[i]-y), (xd[i]-x))
                d = mt.sqrt((xd[i]-x)**2 + (yd[i]-y)**2)
                print(d)

                thetae = (theta - thetad)
                if(thetae > 3.1416):
                    thetae = thetae - 2 * 3.1416
                elif (thetae < 3.1416):
                    thetae = thetae + 2 * 3.1416
                
                w = -kpr * thetae
                v = vMax * mt.tanh(d*kpt/vMax)

                vr = v + (wheelBase*w)/2
                vl = v - (wheelBase*w)/2

                v = (vr + vl) / 2

                vF = wheelRadius*(wR + wL)/2
                wF = wheelRadius * (wR - wL) / wheelBase

                #Compute robot motion
                vx = vF * mt.cos(theta)
                vy = vF * mt.sin(theta)

                x = x + vx * dt
                y = y + vy * dt
                theta = theta + wF * dt

                pV.linear.x = v
                pV.angular.z = w
                vPub.publish(pV)

                if(color == "Red"):
                    pV.linear.x = 0
                    pV.angular.z = 0
                    vPub.publish(pV)
                elif(color == "Yellow"):
                    pV.linear.x = 0.15
                    pV.angular.z = w
                    vPub.publish(pV)
                else:
                    print("Sigo")

                t = t + dt

                rate.sleep()

            #i = i + 1
        
        pV.linear.x = 0
        pV.angular.z = 0
        vPub.publish(pV)
        rospy.signal_shutdown("Over")