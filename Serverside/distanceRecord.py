import serial
import sys
import glob
rssis = []
distances = []
try:
    while True:
        print("Enter the distance (in feet): ")
        dist = input()
        print("Enter the amount of trails you would like to collect")
        quantity = input()
        for num in range(int(quantity)):
            with serial.Serial('/dev/tty.usbmodem14201', 115200, timeout=4) as ser:
                line = ser.readline()   # read a '\n' terminated line
                rssi = line.decode().rstrip().split(",")[0]
                if(rssi != ''):
                    rssis.append(int(rssi) * -1)
                    distances.append(int(dist)  * 0.3048)
                    print(str(int((num + 1)/(int(quantity))*100)) + "%")
except:
    for num in range(len(rssis)):
        print(str(distances[num]) + "," + str(rssis[num]))
#Variation: 19%
#Right: 67
#Forward: 80
#Left: 70
#Back: 80
#up: 68
#Down: 69

#Variation: 19%
#Right: 82
#Forward: 70
#Left: 
#Back: 
#up: 
#Down: 