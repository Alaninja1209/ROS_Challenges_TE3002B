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

def lane_detector(img, vectexs):
        mask = np.zeros_like(img)

        cv.fillPoly(mask, vectexs, 255)

        mask_img = cv.bitwise_and(img, mask)

        return mask_img

def drawLines(img, lines):
    img = np.copy(img)

    blank_image = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)

    for i in lines:
        for x1, x2, y1, y2 in i:
            cv.line(blank_image,(x1,y1),(x2,y2),(255,0,255),thickness=7)

    img = cv.addWeighted(img,0.8,blank_image,1,0.0)

    return img

def define_roi(img, vertexs):
    mask = np.zeros(img)

    cv.fillPoly(mask, vertexs, 255)

    masked_img = cv.bitwise_and(img, mask)

    return masked_img
    
# Define a function to show the image in an OpenCV Window
def show_image(img):
    img = cv.flip(img, 0)  # Gira horizontalmente

    height = img.shape[0]
    width = img.shape[1]

    roi_vertices = [(0,height),(5*width/10,6.8*height/10),(width,height)]

    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    canny = cv.Canny(gray, 100, 150)

    dilated = cv.dilate(canny, (7,7), iterations=3)

    img_prcss = define_roi(dilated,np.array([roi_vertices],np.int32))

    lines = cv.HoughLinesP(
            img_prcss,
            rho=8,
            threshold=1,
            theta=np.pi/180,
            minLineLength=300,
            maxLineGap=0,
            lines=np.array([])
            )
    
    img = drawLines(img_prcss,lines)

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