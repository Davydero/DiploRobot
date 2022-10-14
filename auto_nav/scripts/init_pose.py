#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

#Node initialization
rospy.init_node('init_pose') #nombre del nodo
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 1)
#usaremos un publicador porque nosotros publicaremos en vez de Rviz la pose inicial ('topico', tipo de mensaje, queue)
#Construct message
init_msg = PoseWithCovarianceStamped() #init_msg es del tipo PoseWithCovarianceStamped
init_msg.header.frame_id = 'map'#init_msg tiene un componente llamado header que a su vez tiene un componente llamado frame_id
#toda la parte anterior es para imitar el mensaje que produce Rviz

#Get initial pose from Gazebo
#necesitamos la ayuda de Gazebo para determinar donde es la pose inicial, gazebo tiene un topico llamado odom el cual tiene toda la informacion de velocidades y pose
#del topico /odom tomamos ciertos valores 
odom_msg = rospy.wait_for_message('/odom', Odometry) #necesitamos suscribirnos al topico /odom, este comando permite que el programa se congele hasta que llegue el primer mensaje del topico /odom
init_msg.pose.pose.position.x = odom_msg.pose.pose.position.x #obtenemos los componentes del topico /odom para mandar nuestro propio mensaje
init_msg.pose.pose.position.y = odom_msg.pose.pose.position.y
init_msg.pose.pose.orientation.x = odom_msg.pose.pose.orientation.x
init_msg.pose.pose.orientation.y = odom_msg.pose.pose.orientation.y
init_msg.pose.pose.orientation.z = odom_msg.pose.pose.orientation.z
init_msg.pose.pose.orientation.w = odom_msg.pose.pose.orientation.w

#Delay
rospy.sleep(1)

#Publish message
rospy.loginfo('setting initial pose') #solo es un print
pub.publish(init_msg) #con esto publicamos el mensaje
rospy.loginfo('initial pose is set')