#!/usr/bin/env python3

import rospy
import actionlib #es un tipo especial de servicio, en el codigo estaremos haciendo un cliente que requiera servicios de este servidor, este servidor cumple ciertas tareas como enviar comandos al move base package,,, manda los goal commands al move base package o move base node
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal #move base es nuestro modulo de control, importaremos los dos tipos de mensajes

#Callbacks definition

def active_cb(extra):
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
    rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result): #status definido por el creador de la funcion
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")


rospy.init_node('goal_pose') #inicializacion del nodo

navclient = actionlib.SimpleActionClient('move_base', MoveBaseAction) #definimos lo que es el cliente (es un cliente o servicio especial). Usaremos el servicio llamado move_base y el mensaje sera MoveBaseAction
navclient.wait_for_server() #se esperara al servidor hasta que este disponible

#Example of navigation goal
goal = MoveBaseGoal() #en lo siguiente se determina los componenres del MoveBaseGoal, son las coordenadas de la pose a la que se quiere llegar
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now() #timestamp que graba el momento en el que este mensaje fue creado

goal.target_pose.pose.position.x = -2.16
goal.target_pose.pose.position.y = 0.764
goal.target_pose.pose.position.z = 0.0
goal.target_pose.pose.orientation.x = 0.0
goal.target_pose.pose.orientation.y = 0.0
goal.target_pose.pose.orientation.z = 0.662
goal.target_pose.pose.orientation.w = 0.750

navclient.send_goal(goal, done_cb, active_cb, feedback_cb)# el cliente enviara el goal message y esto incluye 3 callbacks 
finished = navclient.wait_for_result() #el codigo se congela hasta que el cliente reciba un resultado

if not finished:
    rospy.logerr("Action server not available")
else:
    rospy.loginfo(navclient.get_result())
