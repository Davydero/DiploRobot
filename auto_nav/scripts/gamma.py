#!/usr/bin/env python3

import rospy
import random
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('gamma', String, queue_size= 10)
    rospy.init_node('Sensor', anonymous= True)
    print ('nodo creado con exito')
    rate = rospy.Rate(10) #se ejecuta 10 veces por segundo
    while not rospy.is_shutdown():
        lectura = random.gauss(0.2, 0.02)
        lectura = round(lectura,2)
        lectura = str(lectura)
        pub.publish(lectura)
        print(lectura)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
