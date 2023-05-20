#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String

import cv2 as cv
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

# Initialize the ROS Node named 'opencv_example', allow multiple nodes to be run with this name
rospy.init_node('saveVideo', anonymous=True)

# Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
rospy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

# Define a function to show the image in an OpenCV Window
def show_image(img):
    img = cv.flip(img, 0)  # Gira horizontalmente

    cv.imshow("Image Window", img)
    cv.waitKey(3)

# Define a callback for the Image message
def image_callback(img_msg):
    # Log some info about the image topic
    rospy.loginfo(img_msg.header)

    # Try to convert the ROS Image message to a CV2 Image
    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError as e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    # Flip the image 90deg
    # cv_image = cv2.transpose(cv_image)
    cv_image = cv.flip(cv_image, 1)

    # Show the converted image
    show_image(cv_image)

    # Write the image to video
    out.write(cv_image)

# Initialize a subscriber to the "/camera/rgb/image_raw" topic with the function "image_callback" as a callback
sub_image = rospy.Subscriber("video_frames", Image, image_callback)
#sub_image = rospy.Subscriber("/video_source/raw", Image, image_callback)

# Initialize an OpenCV Window named "Image Window"
cv.namedWindow("Image Window", 1)

# Video recording parameters
video_width = 640
video_height = 480
fps = 30.0
output_file = 'output_Test.avi'

# Initialize the video writer
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(output_file, fourcc, fps, (video_width, video_height))

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
    try:
        rospy.spin()
    except KeyboardInterrupt:
        break

# Finalize the video recording and release resources
out.release()
cv.destroyAllWindows()