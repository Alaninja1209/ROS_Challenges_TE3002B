#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import math as mt

error = 0.0
pV = Twist()
pub_velocity = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

def TL_Detector(color, distance, movement):
    # Return two values for x and z

    if color == "red" and distance < 400 and movement == 'forward':
        return 0.0, 0.0  
        
    if color == "yellow" and distance > 400 and movement == 'forward':
        return 0.1, None  
        
    if color == "yellow" and distance < 400:
        return 0.0, 0.0  
        
    if color == "green" and movement == 'forward':
        return 0.285, None  
        
    if color == "stop" and distance < 200:
        return 0.0, 0.0  
        
    if color == "red" and distance < 400 and movement == 'turn':
        return 0.0, 0.0  
        
    if color == "yellow" and distance > 400 and movement == 'turn':
        return 0.1, None  
        
    if color == "yellow" and distance < 400:
        return 0.0, 0.0  
        
    return 0.0, 0.0  

def turn_right():
    pV.linear.z = 15.0

    pub_velocity.publish(pV)

def turn_left():
    pV.linear.z = -15.0

    pub_velocity.publish(pV)

def stop():
    pV.linear.x = 0.0
    pV.linear.z = 0.0

    pub_velocity.publish(pV)

def go_on():
    pV.linear.x = 20.0

    pub_velocity.publish(pV)

def give_way():
    t = 0

    while(t < 3):
        pV.linear.x = 8.0
        pub_velocity.publish(pV)

        t += 0.1

def lane_error_callback(data):
    global error
    error = data.data

if __name__=='__main__':
    rospy.init_node("follow_it", anonymous=True)
    rate = rospy.Rate(100)

    sub_vision_error = rospy.Subscriber("/lane_error", Float32, lane_error_callback)

    pV.linear.x = 0.0
    pV.linear.y = 0.0
    pV.linear.z = 0.0
    pV.angular.x = 0.0
    pV.angular.y = 0.0
    pV.angular.z = 0.0

    last_error = 0.0
    integral = 0.0

    kp = 0.6
    kd = 2 * mt.sqrt(kp)

    #t = 0
    #dt = 0.1

    last_time = rospy.get_time()

    while not rospy.is_shutdown():
        current_t = rospy.get_time()
        dt = current_t - last_time
        last_time = current_t

        prop = kp * error
        der = kd * (error - last_error) / dt

        w = prop + der

        print(w)

        if w >= 0.35:
            w = 2.4
        elif w <= -0.35:
            w = -2.2
        
        if error > 55 or error < -55.0:
            pV.linear.x = 0.10
        else:
            pV.linear.x = 0.15
            w = 0
        
        pV.angular.z = w
        pub_velocity.publish(pV)

        last_error = error