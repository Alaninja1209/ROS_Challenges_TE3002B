#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String

import cv2 as cv
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
rospy.init_node('opencv_example', anonymous=True)

# Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
rospy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

def detectColor(img):
    pub = rospy.Publisher("/color", String, queue_size=10)
    color = String()

    font = cv.FONT_HERSHEY_SIMPLEX
    cimg = img
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # color range
    lower_red1 = np.array([0,100,100])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([160,100,100])
    upper_red2 = np.array([180,255,255])
    lower_green = np.array([40,50,50])
    upper_green = np.array([90,255,255])
    # lower_yellow = np.array([15,100,100])
    # upper_yellow = np.array([35,255,255])
    lower_yellow = np.array([15,150,150])
    upper_yellow = np.array([35,255,255])
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    maskg = cv.inRange(hsv, lower_green, upper_green)
    masky = cv.inRange(hsv, lower_yellow, upper_yellow)
    maskr = cv.add(mask1, mask2)

    size = img.shape
    # print size

    # hough circle detect
    r_circles = cv.HoughCircles(maskr, cv.HOUGH_GRADIENT, 1, 80,
                               param1=50, param2=10, minRadius=0, maxRadius=30)

    g_circles = cv.HoughCircles(maskg, cv.HOUGH_GRADIENT, 1, 60,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)

    y_circles = cv.HoughCircles(masky, cv.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=5, minRadius=0, maxRadius=30)

    # traffic light detect
    r = 5
    bound = 4.0 / 10
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))

        for i in r_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += maskr[i[1]+m, i[0]+n]
                    s += 1
            if h / s > 50:
                cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv.putText(cimg,'RED',(i[0], i[1]), font, 0.5,(255,0,0),1,cv.LINE_AA)
                print("RED: 0")
                color.data = 'Red'
                pub.publish(color)

    if g_circles is not None:
        g_circles = np.uint16(np.around(g_circles))

        for i in g_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += maskg[i[1]+m, i[0]+n]
                    s += 1
            if h /s > 100:
                cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv.circle(maskg, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv.putText(cimg,'GREEN',(i[0], i[1]), font, 0.5,(255,0,0),1,cv.LINE_AA)
                print("GREEN: 1")
                color.data = 'Green'
                pub.publish(color)
                

    if y_circles is not None:
        y_circles = np.uint16(np.around(y_circles))

        for i in y_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += masky[i[1]+m, i[0]+n]
                    s += 1
            if h / s > 50:
                cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv.circle(masky, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv.putText(cimg,'YELLOW',(i[0], i[1]), font, 0.5,(255,0,0),1,cv.LINE_AA)
                print("YELLOW: 0")
                color.data = 'Yellow'
                pub.publish(color)

    cv.imshow('detected results', cimg)
    # cv.imwrite('Computer_Vision\Tests\TrafficLightDetector\Light\Result', cimg)
    # cv.imshow('maskr', maskr)
    # cv.imshow('maskg', maskg)
    # cv.imshow('masky', masky)

    cv.waitKey(3)
    #cv.destroyAllWindows()

# Define a function to show the image in an OpenCV Window
def show_image(img):

    img = cv.flip(img, 0) #Gira horizontalmente

    detectColor(img)

    cv.imshow("Image Window", img)
    cv.waitKey(3)

# Define a callback for the Image message
def image_callback(img_msg):
    # log some info about the image topic
    rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    # Flip the image 90deg
    #cv_image = cv2.transpose(cv_image)
    cv_image = cv.flip(cv_image,1)

    # Show the converted image
    show_image(cv_image)

# Initalize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
#sub_image = rospy.Subscriber("video_frames", Image, image_callback)
sub_image = rospy.Subscriber("/video_source/raw", Image, image_callback)

# Initialize an OpenCV Window named "Image Window"
cv.namedWindow("Image Window", 1)

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
    rospy.spin()