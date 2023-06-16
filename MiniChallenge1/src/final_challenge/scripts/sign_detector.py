#! /usr/bin/env python

import cv2 as cv
import rospy
import numpy as np

from std_msgs.msg import Int32MultiArray, Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node('sign_detector', anonymous=True)

# Print "Hello ROS!" to the Terminal and to a ROS Log file located in ~/.ros/log/loghash/*.log
#rospy.loginfo("Hello ROS!")

# Initialize the CvBridge class
bridge = CvBridge()

def load_model():
    classes = None
    with open(r'\src\final_challenge\scripts\classes', 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
        f.close()
    return classes

def load_classes(classes_path):
    classes = None
    with open(classes_path, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
        f.close()
    return classes

def detect_signs(yolo_model, yolo_output_layer, image):
    img_height = image.shape[0]
    img_width = image.shape[1]
    blob = cv.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    yolo_model.setInput(blob)
    output_layers = yolo_model.forward(yolo_output_layer)
    return output_layers, img_width, img_height

def post_process(frame, output_layers, classes, confidence_threshold=0.5):
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    
    class_ids_list = []
    boxes_list = []
    confidences_list = []
    
    for output_layer in output_layers:
        for detection in output_layer:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > confidence_threshold:
                predicted_class_label = classes[class_id]
                bounding_box = detection[0:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (start_x, start_y, box_width, box_height) = bounding_box.astype("int")
                
                class_ids_list.append(class_id)
                boxes_list.append([start_x, start_y, box_width, box_height])
                confidences_list.append(confidence)
    
    indices = cv.dnn.NMSBoxes(boxes_list, confidences_list, confidence_threshold, 0.3)

def sign_detector(img):
    yolo_cfg_path = "model/yolov4-tiny-custom.cfg"
    yolo_weights_path = "model/yolov4-tiny-custom_best.weights"
    classes_path = "model/classes.names"

    classes = load_classes(classes_path)
    yolo_model = load_model(yolo_cfg_path, yolo_weights_path)
    yolo_output_layer = yolo_model.getUnconnectedOutLayersNames()

    output_layers, img_width, img_height = detect_signs(yolo_model, yolo_output_layer, img)
    post_process(img, output_layers, classes)

# Define a function to show the image in an OpenCV Window
def show_image(img):

    img = cv.flip(img, 0) #Gira horizontalmente

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
sub_image = rospy.Subscriber("/video_source/raw", Image, image_callback)

# Loop to keep the program from shutting down unless ROS is shut down, or CTRL+C is pressed
while not rospy.is_shutdown():
    rospy.spin()