#!/usr/bin/env python3

import rospy
import random
from std_msgs.msg import String
from tf import transformations
import math

def talker():
    pub = rospy.Publisher('quat', String, queue_size= 10)
    rospy.init_node('transformador', anonymous= True)
    print ('nodo creado con exito')
    rate = rospy.Rate(3) #se ejecuta 10 veces por segundo
    while not rospy.is_shutdown():
        quaternion = transformations.quaternion_from_euler(0,0, 0, 'ryxz')
        #angles = transformations.euler_from_quaternion([0,0,0.662,0.75])
        pub.publish(quaternion)
        print(quaternion)
        #pub.publish(angles)
        #print(angles)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

#para 90 grados en z  [0.         0.         0.70710678 0.70710678]
# para 180 grados en z [0.000000e+00 0.000000e+00 1.000000e+00 6.123234e-17]
#para 270 grados en z [ 0.         -0.          0.70710678 -0.70710678]