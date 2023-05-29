#!/usr/bin/env python2
import rospy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError

class Lane_detector:
    def __init__(self):
        self.base_pixel = 240

        self.rate = rospy.Rate(50)

        self.bridge = CvBridge()

        self.pub_lane_error = rospy.Publisher("/lane_error", Float32, queue_size=10)

        self.sub_image = rospy.Subscriber("/video_source/raw", Image, self.image_callback)

        rospy.init_node('lane_detector', anonymous=True)
    
    def preprocess(self, img):
        # Resize image
        img_rs = cv.resize(img, (480, 480))

        gray = cv.cvtColor(img_rs, cv.COLOR_BGR2GRAY)

        gray_blur = cv.blur(gray, (13,13))

        return gray_blur
    
    def define_roi(self, img):
        return img[430:480, 0:480]
    
    def draw_it(self, func):
        cl_points = []
        for i in range(len(func) - 1):
            cl_points.append((func[i + 1] - 2 * func[i] + func[i]) / (i - (i - 1)))
        cl_points.append(0)

        return cl_points
    
    def calculate_min_lines(self, grad):
        left_array = grad[:50]
        center_array = grad[51:429]
        right_array = grad[430:]

        left_min_index = np.where(left_array == np.amin(left_array))[0][0]
        center_min_index = np.where(center_array == np.amin(center_array))[0][0] + 50
        right_min_index = np.where(right_array == np.amin(right_array))[0][0] + 430

        return left_min_index, center_min_index, right_min_index
    
    def calculater_center_line(self):
        preproccess_img = self.preprocess(img=self.cv_image)

        roi_region = self.define_roi(img=preproccess_img)

        vertical_sum = roi_region.sum(axis=0)

        grad = self.draw_it(vertical_sum)

        left_min, right_min, center_min = self.calculate_min_lines(grad)

        self.error = self.base_pixel - center_min

        self.pub_lane_error.publish(Float32(self.error))

    # Define a callback for the Image message
    def image_callback(self, img_msg):
        # Try to convert the ROS Image message to a CV2 Image
        try:
            self.cv_image = cv.flip(self.bridge.imgmsg_to_cv2(img_msg))
            #cv_image = cv.flip(cv_image,1)

        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
    ld = Lane_detector()
    ld.calculater_center_line()

    rospy.spin()