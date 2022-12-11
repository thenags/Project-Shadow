import subprocess
import sys
import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('schooltracking-40411-firebase-adminsdk-9hzh4-80588df601.json')
#TO-DO - Instead of writing to the database for each student, save the student data in a variable and write to it for each student, then upload the overall data in the end
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://schooltracking-40411-default-rtdb.firebaseio.com'
})

def convertToString(bssids, rssis):
    finalString = ""
    for (num, rssi) in enumerate(rssis):
        finalString += str(rssi)+","+str(bssids[num])+" "
    return finalString
def getPosition(data, emergency):
    programResult = subprocess.run(['python3', 'positioner.py', data, str(emergency)], stdout=subprocess.PIPE)
    if("ERROR" in programResult.stdout.decode().strip()):
        return -1
    results = programResult.stdout.decode().strip().split(" ")
    return results
def setNewPosition(results, id):
    studentRef = db.reference('students')
    x = results[0]
    y = results[1]
    rad = results[2]
    studentRef.child(id).child("position").update({
        '0': float(x),
        '1': float(y),
        '2': float(rad)
    })
    studentRef.child(id).child("details").update({
        '0': results[3] == "True",
    })
def getPeriod(hour, minute):
    if hour == 7:
        if minute >= 40:
            return 1
    elif hour == 8:
        if minute <= 27:
            return 1
        elif minute >= 32:
            return 2
    elif hour == 9:
        if minute <= 14:
            return 2
        elif minute >= 19:
            return 3
    elif hour == 10:
        if minute <= 1:
            return 3
        elif minute >= 6 and minute <= 48:
            return 4
        elif minute >= 53:
            return 5
    elif hour == 11:
        if minute <= 35:
            return 5
        elif minute >= 40:
            return 6
    elif hour == 12:
        if minute <= 22:
            return 6
        elif minute >= 27:
            return 7
    elif hour == 13:
        if minute <= 9:
            return 7
        elif minute >= 14 and minute <= 56:
            return 8
    else:
        return 9
try:
    while True:
        studentRef = db.reference('students')
        studentData = studentRef.get()
        settingsRef = db.reference('settings')
        settingsData = settingsRef.get()
        now = datetime.datetime.now()
        period = getPeriod(now.hour, now.minute)
        settingsRef.update({
            '2': period,
        })
        settingsRef.update({
            '3': int(settingsData[3]) + 1,
        })
        totalTime = 0
        for id in studentData:
            #0 - no situation
            #1 - lock out
            #2 - lock down
            #SETTINGS:
            #    0 - EMERGENCY STATE
            #    1 - STUDENTS IN DANGER
            #    2 - PERIOD
            #    3 - Server status timer
            begin = time.time()
            list = convertToString(studentData[id]['wapBSSIDS'], studentData[id]["wapRSSIS"])
            position = getPosition(list, int(settingsData[0]) - 1)
            if(position != -1):
                setNewPosition(position, id)
            end = time.time()
            totalTime += (end - begin)
        print(totalTime)
        if(totalTime < 15):
            time.sleep(15 - totalTime)
except:
    print("Looping ended")