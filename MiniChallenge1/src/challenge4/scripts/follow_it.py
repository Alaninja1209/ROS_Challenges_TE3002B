import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import math as mt

#Declared variables of ros suscriber
wR = 0.0
wL = 0.0

def wr_callback(data):
    global wR
    wR = data.data

def wl_callback(data):
    global wL
    wL = data.data

def vision_error_callback(data):
    error = data.data

def follow_lane():
    kpt = 40
    kpr = 2 * mt.sqrt(kpt)

    t = t + dt

    prop = kpt * error
    der = kpr * (error - last_error) / dt

    w = prop + der

    if w >= 0.15:
        w = 0.15
    elif w <= -0.15:
        w = -0.15
    
    if error > 55 or error < -55.0:
        pV.linear.x = 0.1
    else:
        pV.linear.x = 0.20
        w = 0
    
    pV.angular.z = w
    pub_velocity.publish(pV)

    last_error = error

    rate.sleep()


if __name__=='__main__':
    rospy.init_node("follow_it", anonymous=True)
    rate = rospy.Rate(100)

    sub_vision_error = rospy.Subscriber("/vision_error", Float32, vision_error_callback)
    pub_velocity = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    pV = Twist()
    pV.linear.x = 0.0
    pV.linear.y = 0.0
    pV.linear.z = 0.0
    pV.angular.x = 0.0
    pV.angular.y = 0.0
    pV.angular.z = 0.0

    error = 0.0
    last_error = 0.0
    integral = 0.0

    t = 0
    dt = 0.01

    while not rospy.is_shutdown():
        follow_lane()