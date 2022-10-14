#!/usr/bin/env python3

from asyncore import read
import rospy
import actionlib #es un tipo especial de servicio, en el codigo estaremos haciendo un cliente que requiera servicios de este servidor, este servidor cumple ciertas tareas como enviar comandos al move base package,,, manda los goal commands al move base package o move base node
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal #move base es nuestro modulo de control, importaremos los dos tipos de mensajes
from std_msgs.msg import String

import time
import tkinter # para el GUI
import threading #para hilos

from fpdf import FPDF


# se creara la lista con las coordenadas x y y para los puntos que se desea cubrir con el robot
posX = [3,       5,   7,    1,   -1,   -3,   -4,  -4,-5.5, -4,  -2,   0,   2,   4,   6,   8, 8.5, 8.5, 8.5, 8.5, 8.5, 3]
posY = [-2.6, -2.6,-2.6, -2.6, -2.6, -2.6, -0.3, 1.5, 3.5,  6, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5,   6,   4,   2,   0,  -2, -3]
orZ = [0.707, 0.707, 0.707, 0.707, 0.707, 0.707, 0, 0, 0, 0, 0.707, 0.707, 0.707, 0.707, 0.707, 0.707,1,1,1,1,1,0]
orW = [0.707, 0.707, 0.707,0.707, 0.707, 0.707, 1, 1, 1, 1, -0.707, -0.707, -0.707, -0.707, -0.707, -0.707,0,0,0,0,0,1]


posIX = [-1.7, -1.7, -1.7, -1.7, -1.7, -0.5, 1.5, 3.5, 5.5, 0.8, 0.8, 0.8, 2.8, 4.8,  3]
posIY = [-2,     0,     2,    4,    5,    5,   5,   5,   5, 3.5,   2, 0.5, 0.5, 0.5, -3]
orIZ = [0.707, 0, 0, 0, 0,0, 0.707,0.707, 0.707,0,0,0, 0.707, 0.707, 0.707]
orIW = [0.707,1,1,1,1,1,-0.707, -0.707, -0.707,1,1,1, 0.707, 0.707, 0.707]

lecturasEx = [[0,0,0]]
lecturasIn = [[0,0,0]]


for m in range(len(posX)-2):
    lecturasEx.append([0,0,0])

for m in range(len(posIX)-2):
    lecturasIn.append([0,0,0])

lecSensor = 0
parar = 0

class PDF(FPDF):
    pass
    def logo(self, name, x, y, w, h):
        self.image(name, x, y, w, h)
    
    def texts(self, name):
        with open(name, 'rb') as xy:
            txt = xy.read.decode('latin-1')
        self.set_xy(10.0, 80.0)
        self.set_text_color(76.0, 32.0, 250.0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, txt)
    
    def titles(self, title):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align='C', txt=title, border = 0)
    
    def matrices(self, matriz):
        self.set_xy(20.0, 150)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt=matriz, border = 0)

#Callbacks definition 
def active_cb(extra):
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
    rospy.loginfo("Current location: "+str(feedback))
    rospy.loginfo("Lecturas Int:"+str(lecturasIn))
    rospy.loginfo("Lecturas Ext"+str(lecturasEx))

def done_cb(status, result): #status definido por el creador de la funcion
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")

def lectura(data):
    global lecSensor
    lecSensor = data.data


rospy.init_node('goal_pose') #inicializacion del nodo

navclient = actionlib.SimpleActionClient('move_base', MoveBaseAction) #definimos lo que es el cliente (es un cliente o servicio especial). Usaremos el servicio llamado move_base y el mensaje sera MoveBaseAction
navclient.wait_for_server() #se esperara al servidor hasta que este disponible
rospy.Subscriber('gamma', String, lectura)

def internoWorker():
    global lecturasIn
    global lecSensor
    for i in range(len(posIX)):
        goal = MoveBaseGoal() #en lo siguiente se determina los componenres del MoveBaseGoal, son las coordenadas de la pose a la que se quiere llegar
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() #timestamp que graba el momento en el que este mensaje fue creado

        goal.target_pose.pose.position.x = posIX[i]
        goal.target_pose.pose.position.y = posIY[i]
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0  #quaternion obtenido mediante otro programa
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = orIZ[i]
        goal.target_pose.pose.orientation.w = orIW[i]

        navclient.send_goal(goal, done_cb, active_cb, feedback_cb)# el cliente enviara el goal message y esto incluye 3 callbacks 
        finished = navclient.wait_for_result() #el codigo se congela hasta que el cliente reciba un resultado

        if not finished:
            rospy.logerr("Action server not available")
        else:
            rospy.loginfo(navclient.get_result())
        if parar == 1:
            break
        if i < len(posIX)-1:
            for j in range(3):
                lecturasIn[i][j]= lecSensor
                time.sleep(1)
        
        print(parar)




def externoWorker():
    global lecturasEx
    global lecSensor
    for i in range(len(posX)):
        goal = MoveBaseGoal() #en lo siguiente se determina los componenres del MoveBaseGoal, son las coordenadas de la pose a la que se quiere llegar
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() #timestamp que graba el momento en el que este mensaje fue creado

        goal.target_pose.pose.position.x = posX[i]
        goal.target_pose.pose.position.y = posY[i]
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = orZ[i]
        goal.target_pose.pose.orientation.w = orW[i]

        navclient.send_goal(goal, done_cb, active_cb, feedback_cb)# el cliente enviara el goal message y esto incluye 3 callbacks 
        finished = navclient.wait_for_result() #el codigo se congela hasta que el cliente reciba un resultado

        if not finished:
            rospy.logerr("Action server not available")
        else:
            rospy.loginfo(navclient.get_result())
        if parar == 1:
            break
        if i < len(posX)-1:
            for j in range(3):
                lecturasEx[i][j]= lecSensor
                time.sleep(1)



def pararWorker():
    for i in range(len(posX)):
        goal = MoveBaseGoal() #en lo siguiente se determina los componenres del MoveBaseGoal, son las coordenadas de la pose a la que se quiere llegar
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() #timestamp que graba el momento en el que este mensaje fue creado

        goal.target_pose.pose.position.x = 3
        goal.target_pose.pose.position.y = -3
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
        

#Example of navigation goal
def interno():
    global parar
    parar = 0 
    t = threading.Thread(target= internoWorker)
    t.start()

def externo():
    global parar
    parar = 0 
    u = threading.Thread(target= externoWorker)
    u.start()

def parare():
    global parar
    global lecturasIn
    global lecturasEx
    print(lecturasIn)
    print(lecturasEx)
    parar = 1 
    p = threading.Thread(target= pararWorker)
    p.start()

def Reporte():
    pdf = PDF()
    pdf.add_page()
    pdf.titles("Reporte Monitoreo Radiologico Centro de Radiacion Gamma")
    pdf.logo('/home/davy/catkin_ws/src/auto_nav/scripts/Calliope2.JPG', 30, 30, 150,120)

    datain = [["Lectura 1 [uSv/hr]", "Lectura 2 [uSv/hr]", "Lectura3 [uSv/hr]"]]
    for l in range(len(lecturasIn)):
        datain.append(lecturasIn[l])
    #print(datain)
    filanum = ["Punto"]
    for r in range(len(lecturasIn)):
        filanum.append(r+1)
    pdf.add_page()
    pdf.titles("Mediciones internas")
    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 2.5
    col_width = 30 # distribute content evenly
    desfasey = 0
    pdf.set_xy(100,50)
    for fila in range(len(filanum)):
        pdf.set_xy(50,desfasey+50)
        pdf.multi_cell(15, line_height, str(filanum[fila]), 1, 0)
        desfasey = desfasey+line_height
    desfasey = 0
    pdf.set_xy(100, 50)
    for row in datain:
        desfasex = 30
        for datum in row:
            pdf.set_xy(desfasex+35,desfasey+50)
            desfasex = desfasex+col_width
            pdf.multi_cell(col_width, line_height, str(datum), 1, 0)
        pdf.ln(line_height)
        desfasey = desfasey+line_height


    dataex = [["Lectura 1 [uSv/hr]", "Lectura 2 [uSv/hr]", "Lectura3 [uSv/hr]"]]
    for l in range(len(lecturasEx)):
        dataex.append(lecturasEx[l])
    #print(dataex)
    filanum = ["Punto"]
    for r in range(len(lecturasEx)):
        filanum.append(r+1)
    pdf.add_page()
    pdf.titles("Mediciones Externas")
    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 2.5
    col_width = 30 # distribute content evenly
    desfasey = 0
    pdf.set_xy(100, 50)
    for fila in range(len(filanum)):
        pdf.set_xy(50,desfasey+50)
        pdf.multi_cell(15, line_height, str(filanum[fila]), 1, 0)
        desfasey = desfasey+line_height
    desfasey = 0
    pdf.set_xy(100, 50)
    for row in dataex:
        desfasex = 30
        for datum in row:
            pdf.set_xy(desfasex+35,desfasey+50)
            desfasex = desfasex+col_width
            pdf.multi_cell(col_width, line_height, str(datum), 1, 0)
        pdf.ln(line_height)
        desfasey = desfasey+line_height

    pdf.set_author('Davy Rojas')
    pdf.output('test.pdf', 'F')

#GUI 
ventana =  tkinter.Tk()
ventana.geometry("400x300")
etiqueta = tkinter.Label(ventana, text = "Robot Monitoreo Radiologico")
etiqueta.pack()
startIn = tkinter.Button(ventana, text="Inicio Interno", command = interno)
startIn.pack()
startExt = tkinter.Button(ventana, text="Inicio Externo", command = externo)
startExt.pack()
stop = tkinter.Button(ventana, text= "Stop", command = parare)
stop.pack()
reporte = tkinter.Button(ventana, text= "Reporte", command = Reporte)
reporte.pack()
ventana.mainloop() 