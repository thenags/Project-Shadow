from tkinter import *
import tkinter as tk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import math
import time
import numpy as np
import serial
import random
#0.002 0.098
#0.002 0.099
#0.002 0.099
#0.002 0.094
#0.001 0.096
#0.003 0.098

#15/15
# START RSSI TO DISTANCE CODE
meterScale = 4.658
#BI-DIRECTIONAL
#a = 0.0255
#b = 0.0735
#OMNIDIRECTIONAL
a = 0.02
b = 0.07
#0.0355
#0.067
class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
c = 4.96
environmentalFactor = 2.4
meterRSSI = -56
mouseX = 0
mouseY = 0
rssiError = 20
sessionPoints = []
sessionRSSIS = []
sessionBSSIDS = []
schoolBorders = []
pointA = []
pastPoints = []
#['84:F7:03:EA:D1:A9', '84:F7:03:EA:CD:01', '84:F7:03:EA:D2:5F'] [-74, -75, -76] (center)

roomBSSIDs =  []
roomNums = []
roomPositions = []

def dist(a,b):
    return np.sqrt(int(a[0] - b[0]) *int(a[0] - b[0])  + int(a[1] - b[1]) * int(a[1] - b[1]))
def rssiToDist(rssi):
    #10^((Measured Power - Instant RSSI)/10*N).
    return a * pow(2.71828,(float(rssi) * -1.0 * b)) * meterScale
    #return a * pow(((float(rssi) * -1.0)),b)  * meterScale
   # print((10 ^ ((-67 - (rssi))/10 * 3))/1000)
    #return (10 ^ int((meterRSSI - float(rssi))/10 * environmentalFactor)) * meterScale
#ser = serial.Serial('/dev/tty.usbmodem14201')
# END RSSI TO DISTANCE CODE

# As an admin, the app has access to read and write all data, regradless of Security Rules
#waps = db.reference('waps')
#students = db.reference('students')
foundWaps = [[788, 773, '78:BC:1A:5E:D0:80'], [727, 783, '78:BC:1A:5E:E2:C0'], [482, 721, '78:BC:1A:5E:DD:80'], [519, 657, '78:BC:1A:56:20:A0'], [466, 660, '78:BC:1A:5E:E2:E0'], [426, 669, '78:BC:1A:6B:D3:E0'], [371, 724, '78:BC:1A:6C:EA:E0'], [618, 657, ' 78:BC:1A:56:2B:40'], [627, 720, '78:BC:1A:56:2B:80'], [690, 656, '78:BC:1A:59:1C:20'], [714, 655, 'DC:8C:37:AE:80:40'], [782, 687, '78:BC:1A:57:C0:E0'], [607, 748, '78:BC:1A:52:7F:60'], [436, 754, 'DC:8C:37:AC:69:40'], [525, 754, '78:BC:1A:42:B5:E0'], [829, 714, '78:BC:1A:4D:CA:00'], [579, 789, '78:BC:1A:52:80:80'], [517, 693, 'DC:8C:37:8A:B2:E0'], [428, 722, '78:BC:1A:6C:E5:60'], [482, 732, 'D4:F9:8D:70:F1:2D'], [456, 710, 'D4:F9:8D:70:F1:2B'], [527, 709, 'D4:F9:8D:70:F1:7B'], [512, 667, 'F6:12:FA:41:FD:74'], [470,667,'84:F7:03:EA:D2:17']]
def getWAPpos(bssid):
    global foundWaps
    for wap in foundWaps:
        if wap[2] == bssid:
            return (wap[0],wap[1])



# Create object 
root = Tk()
  
# Adjust size 
root.geometry("970x750")
  
# Add image file
bg = PhotoImage(file = "gchs.png")
  
# Create Canvas
canvas = Canvas( root, width = 970,
                 height = 750)
  
canvas.pack(fill = "both", expand = True)

# Display image
canvas.create_image( 0, 0, image = bg, 
                     anchor = "nw")
for border in schoolBorders:
    canvas.create_line(border[0][0],border[0][1],border[1][0],border[1][1],fill="red",width=3) 

#END VISUALIZATION CODE
p = 0
#showPosition()
#updateStudentPosition("224288","blue")

def motion(event):
    global mouseX, mouseY
    x, y = event.x, event.y
    if(x > 0 and x < 970 and y > 0 and y < 750):
        mouseX = x
        mouseY = y
        #print(mouseX, mouseY)
def leftclick(event):
    global bssids, rssis, a, b, pastPoints, pointA, schoolBorders
    if(pointA != []):
        pointB = [mouseX, mouseY]
        schoolBorders.append([pointA, pointB])
        canvas.create_line(pointA[0],pointA[1],pointB[0],pointB[1],fill="green",width=2) 
        pointA = []
        
    else:
        pointA =[mouseX, mouseY]
def finish(event):
    print(schoolBorders)
root.bind('<Motion>', motion)
root.bind("<Button-1>", leftclick)
root.bind("<Return>", finish)
#showPosition()
try:
    # Execute tkinter
    root.mainloop()
    while True: 
        print("failure")
        time.sleep(0.5)
except:
    print("program cancelled")

    
