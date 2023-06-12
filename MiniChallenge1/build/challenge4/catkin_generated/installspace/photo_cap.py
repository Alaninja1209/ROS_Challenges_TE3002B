#!/usr/bin/env python2
from __future__ import print_function

import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time

class image_converter:
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/video_source/raw", Image, self.callback)
    self.rate = rospy.Rate(30)
    self.num = 0
    self.move_distance = 20  # Distancia de movimiento horizontal

  def callback(self, data):
    try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    # Voltear la imagen verticalmente
    cv_image = cv2.flip(cv_image, 0)

    cv_image = cv2.flip(cv_image, 1)

    frame = cv2.resize(cv_image, (950, 600))
    self.num = self.num + 1
    nombre = 'valS' + str(self.num)

    save = cv2.imwrite('/home/alfredo1209/val/{}.png'.format(nombre), frame)

    time.sleep(1)
    cv2.waitKey(3)

    self.rate.sleep()

def main(args):
  rospy.init_node('video_record_compu')
  ic = image_converter()
  try:
      rospy.spin()
  except KeyboardInterrupt:
      print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

