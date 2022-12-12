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
import sys
#0.002 0.098
#0.002 0.099
#0.002 0.099
#0.002 0.094
#0.001 0.096
#0.003 0.098
testArrays = ["-77,D4:F9:8D:70:F1:2D -80,D4:F9:8D:70:F1:7B -85,F6:12:FA:41:FD:74","-89,D4:F9:8D:70:F1:2D -75,D4:F9:8D:70:F1:7B"]
testArrayNumber = 0
#TO DO
#1) FIX ERROR ON 379 if point[0] < minPoint[0]:

# 95% accuracy, 2.5m error
# 1/45
# 1.18, 3.6, 5.48, 6.04, .97, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 8.8, 8.71, 8.8, 7.41, 7.51, 9.67, 13.11, 5.11, 3.44, 9.5, 9.35, 9.34, 9.45, 0.46, 3.77, 4.94, 1.5, 2.69, 1.5, 3.11, 7.2, 10.52
# ['D4:F9:8D:70:F1:2D', 'D4:F9:8D:70:F1:7B', 'F6:12:FA:41:FD:74'] [-77, -80, -89]

#['D4:F9:8D:70:F1:2D', 'D4:F9:8D:70:F1:7B'] [-85, -93]
# START RSSI TO DISTANCE CODE
meterScale = 4.658
#a = 0.0255
#b = 0.0735
#OMNIDIRECTIONAL
a = 0.02
b = 0.07
#0.0355
#0.067

c = 4.96
environmentalFactor = 2.4
meterRSSI = -56
mouseX = 0
mouseY = 0
rssiError = 25
sessionPoints = []
sessionRSSIS = []
sessionBSSIDS = []
schoolBorders = []
pastX = 0
pastY = 0
pastDist = 0
pastPoints = []
#['84:F7:03:EA:D1:A9', '84:F7:03:EA:CD:01', '84:F7:03:EA:D2:5F'] [-74, -75, -76] (center)
checkPoints = [[373, 682], [373, 682], [373, 689], [373, 689], [373, 697], [373, 697], [400, 698], [400, 698], [399, 688], [398, 689], [397, 677], [397, 677], [425, 698], [424, 692], [423, 680], [423, 682], [425, 688], [443, 687], [444, 690], [444, 695], [445, 698], [442, 676], [442, 676], [465, 688], [465, 688], [466, 696], [464, 698], [486, 683], [486, 700], [487, 697], [494, 689], [496, 689], [519, 687], [519, 687], [517, 677], [517, 677], [515, 697], [515, 697], [557, 676], [557, 678], [557, 687], [556, 694], [589, 695], [589, 692], [587, 675], [589, 676], [589, 684], [591, 685], [627, 694], [627, 694], [625, 684], [626, 684], [650, 694], [650, 694], [648, 684], [648, 685], [647, 675], [647, 675], [679, 675], [679, 675], [680, 684], [680, 684], [679, 692], [679, 692], [713, 692], [713, 692], [712, 685], [715, 687], [709, 675], [714, 676], [744, 678], [744, 678], [746, 686], [746, 686],[539, 655], [545, 698], [490, 686], [470, 682], [425, 698], [424, 687], [423, 678], [448, 687],[534, 655], [506, 670], [505, 641], [551, 640], [558, 663], [544, 678], [545, 699], [593, 694], [609, 677], [633, 695], [680, 676], [706, 692], [732, 674], [761, 683], [784, 692], [799, 732], [766, 732], [766, 657], [792, 656], [489, 700], [527, 703], [527, 729], [503, 719], [470, 731], [470, 707], [479, 676], [455, 679], [445, 700], [432, 675], [419, 703], [389, 679], [423, 685], [468, 687], [569, 687], [656, 685]]
bssids = [['D4:F9:8D:70:F1:2D', 'D4:F9:8D:70:F1:2B', 'F6:12:FA:41:FD:74'], ['78:BC:1A:57:C3:80', '78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0', '78:BC:1A:56:2C:20'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0', '78:BC:1A:57:C3:80'], ['78:BC:1A:57:C3:80', '78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:57:C3:80', '78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0', '78:BC:1A:57:C3:80'], ['78:BC:1A:4D:DD:A0', '78:BC:1A:6B:D7:C0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:4D:DD:A0', '78:BC:1A:57:C3:80'], ['78:BC:1A:4D:DD:A0', '78:BC:1A:57:C3:80', '78:BC:1A:6B:D7:C0'], ['78:BC:1A:4D:DD:A0', '78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:D6:A0'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0', '78:BC:1A:56:2C:20'], ['78:BC:1A:6B:D7:C0', '78:BC:1A:57:C3:80', '78:BC:1A:4D:DD:A0', '78:BC:1A:4D:D6:A0'], ['78:BC:1A:56:2C:20', '78:BC:1A:6B:D7:C0', '78:BC:1A:56:23:E0', '78:BC:1A:57:C3:80'], ['78:BC:1A:6B:E6:E0', '78:BC:1A:6B:D7:C0', '78:BC:1A:56:2C:20', '78:BC:1A:4D:D6:A0'], ['78:BC:1A:4D:D6:A0', '78:BC:1A:4D:DD:A0', 'DC:8C:37:B4:CA:80', '78:BC:1A:6B:E6:E0'], ['78:BC:1A:6B:E6:E0', '78:BC:1A:5E:CF:A0', '78:BC:1A:4D:D6:A0'], ['78:BC:1A:6B:E6:E0', '78:BC:1A:4D:D6:A0', 'DC:8C:37:B4:CA:80', '78:BC:1A:5E:CF:A0', 'DC:8C:37:BC:C4:00'], ['DC:8C:37:B4:CA:80', '78:BC:1A:6B:E6:E0', '78:BC:1A:4D:D6:A0', 'DC:8C:37:BC:C4:00'], ['78:BC:1A:6B:E6:E0', 'DC:8C:37:BC:C4:00'], ['DC:8C:37:BC:C4:00', 'DC:8C:37:B4:CA:80'], ['DC:8C:37:BC:C4:00', '78:BC:1A:6B:DA:40', '78:BC:1A:6B:D1:20', '78:BC:1A:4D:CD:C0'], ['78:BC:1A:6B:D1:20', '78:BC:1A:6B:DA:40', 'DC:8C:37:BC:C4:00'], ['78:BC:1A:6B:D1:20', 'DC:8C:37:BC:C4:00'], ['78:BC:1A:6B:D1:20', 'DC:8C:37:BC:C4:00', '78:BC:1A:6B:DA:40'], ['78:BC:1A:6B:D1:20', '78:BC:1A:6B:DA:40', '78:BC:1A:4D:CD:C0', 'DC:8C:37:BC:C4:00'], ['78:BC:1A:6B:D1:20', '78:BC:1A:6B:DA:40', '78:BC:1A:6B:E6:E0'], ['78:BC:1A:6B:DA:40', '78:BC:1A:6B:D1:20'], ['78:BC:1A:6B:DA:40', '78:BC:1A:6B:D1:20'], ['78:BC:1A:6B:DA:40'], ['78:BC:1A:6B:DA:40', '78:BC:1A:56:2B:C0'], ['78:BC:1A:6B:DA:40'], ['78:BC:1A:6B:DA:40', '78:BC:1A:52:82:E0'], ['78:BC:1A:6B:DA:40', '78:BC:1A:52:B5:60', '78:BC:1A:52:82:E0'], ['78:BC:1A:52:B5:60', '78:BC:1A:6B:DA:40'], ['78:BC:1A:52:B5:60'], ['78:BC:1A:52:B5:60', '78:BC:1A:6B:DA:40'], ['DC:8C:37:BA:D8:60', '78:BC:1A:6B:DA:40'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:52:B5:60'], ['78:BC:1A:59:1A:40'], ['78:BC:1A:59:1A:40'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:59:1A:40'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:E5:60', '78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6B:D3:E0', '78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:5E:E2:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0', '78:BC:1A:5E:E2:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0'], ['78:BC:1A:6C:EA:E0'], ['78:BC:1A:6B:D3:E0', '78:BC:1A:6C:EA:E0', '78:BC:1A:6C:E5:60'], ['78:BC:1A:6C:E5:60', '78:BC:1A:6C:EA:E0', '78:BC:1A:6B:D3:E0', '78:BC:1A:5E:E2:E0'], ['78:BC:1A:6B:D3:E0', '78:BC:1A:6C:E5:60', 'DC:8C:37:AC:69:40', '78:BC:1A:5E:E2:E0', '78:BC:1A:6C:EA:E0'],['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', 'DC:8C:37:C4:52:A0'], ['78:BC:1A:56:20:A0', 'DC:8C:37:C4:52:A0'], ['78:BC:1A:56:20:A0'],['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:57:BE:E0'], ['78:BC:1A:56:20:A0', 'DC:8C:37:C4:52:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', 'DC:8C:37:C4:52:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:56:2B:40'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0', '78:BC:1A:56:2B:40', 'DC:8C:37:C4:52:A0'], ['78:BC:1A:56:20:A0'], ['78:BC:1A:56:20:A0']]
rssis = [[-74, -75, -76], [-73, -77, -77], [-75, -77, -80, -91], [-76, -81, -82], [-73, -74, -83], [-73, -75, -82], [-68, -78, -89], [-77, -84, -85], [-77, -81, -88], [-72, -74, -85], [-70, -77, -77], [-76, -82], [-76, -78, -78], [-67, -81, -83], [-69, -71, -79, -89], [-80, -83, -88, -94], [-69, -78, -86, -94], [-78, -86, -86, -88], [-74, -88, -89, -89], [-80, -88, -89, -89], [-86, -90, -90], [-81, -86, -87, -91, -93], [-82, -84, -84, -89], [-82, -88], [-88, -89], [-81, -86, -88, -91], [-81, -87, -88], [-82, -89], [-84, -89, -92], [-85, -85, -89, -91], [-82, -83, -88], [-85, -87], [-71, -89], [-71], [-61, -83], [-77], [-74, -89], [-85, -90, -92], [-82, -85], [-87], [-91, -91], [-87, -90], [-89, -91], [-88], [-88], [-83, -87], [-86], [-85, -91], [-88], [-88, -89, -90], [-83, -90], [-86], [-89, -90, -92], [-83], [-85, -87], [-86, -91], [-86], [-83, -88], [-83], [-86, -88, -88], [-84, -86, -94], [-81, -88, -91], [-81], [-85, -89, -90], [-86, -89, -89], [-88, -89, -90, -90], [-78, -89, -90, -90], [-82, -87, -87], [-86], [-79, -90], [-80, -91], [-76], [-84, -84, -87], [-79, -83, -84, -90], [-80, -84, -86, -89, -91],[-60], [-70], [-66], [-68], [-69], [-65, -88], [-69, -88], [-65],[-58], [-66], [-74], [-69], [-67], [-64], [-77], [-69], [-68], [-68], [-70], [-65], [-76], [-74], [-63, -88], [-64, -91], [-61, -90], [-57, -87], [-67, -86], [-75], [-74], [-55, -90], [-62], [-68, -89], [-72], [-69], [-68, -88], [-69, -88], [-80], [-72, -87], [-66, -91], [-67], [-72, -87, -91], [-68], [-73]]
roomBSSIDs =  [["D4:F9:8D:70:F1:2D","D4:F9:8D:70:F1:7B"],["D4:F9:8D:70:F1:2B"],["F6:12:FA:41:FD:74"],[""],[""],[""],[""],[""]]
roomNums = [210,212,207,211,209,205,208,206]
roomPositions = [[502,719],[436,720],[532,653],[433,665],[465,657],[598,656],[584,720],[643,720]]
roomBounds = [[468,705,558,1000],[409,705,468,1000],[505,600,564,676],[412,600,452,678],[452,600,506,679],[562,600,633,676],[555,700,612,1000],[612,700,672,1000]]
schoolOutline = [[[170, 292], [359, 225]], [[359, 226], [370, 251]], [[369, 252], [392, 243]], [[392, 245], [396, 256]], [[531, 211], [531, 210]], [[531, 211], [527, 197]], [[527, 197], [463, 150]], [[462, 149], [466, 121]], [[466, 121], [474, 125]], [[474, 125], [503, 85]], [[503, 85], [495, 76]], [[495, 76], [523, 64]], [[523, 64], [547, 82]], [[547, 82], [589, 22]], [[589, 22], [604, 31]], [[604, 31], [611, 21]], [[611, 21], [657, 52]], [[657, 52], [652, 62]], [[650, 62], [664, 73]], [[663, 73], [624, 130]], [[624, 130], [589, 135]], [[589, 135], [577, 151]], [[577, 151], [584, 158]], [[584, 158], [594, 187]], [[594, 187], [688, 153]], [[688, 153], [686, 33]], [[686, 33], [847, 29]], [[847, 29], [848, 24]], [[848, 24], [952, 24]], [[953, 23], [958, 153]], [[958, 153], [954, 154]], [[954, 154], [963, 409]], [[964, 410], [965, 460]], [[965, 460], [921, 464]], [[921, 463], [926, 678]], [[926, 678], [823, 680]], [[823, 680], [817, 492]], [[817, 492], [711, 493]], [[711, 493], [711, 544]], [[711, 544], [498, 547]], [[498, 547], [497, 542]], [[497, 542], [477, 543]], [[477, 543], [476, 534]], [[476, 534], [423, 535]], [[423, 535], [426, 544]], [[426, 544], [264, 599]], [[264, 599], [239, 534]], [[239, 534], [193, 550]], [[193, 550], [238, 680]], [[238, 680], [132, 715]], [[132, 715], [4, 361]], [[4, 361], [108, 319]], [[108, 319], [132, 389]], [[132, 389], [195, 367]], [[195, 368], [170, 291]], [[304, 632], [333, 705]], [[333, 705], [332, 742]], [[332, 742], [804, 739]], [[804, 739], [803, 655]], [[803, 655], [765, 655]], [[763, 655], [762, 636]], [[304, 630], [361, 611]], [[361, 611], [371, 642]], [[371, 642], [762, 636]], [[397, 257], [532, 209]]]
schoolHallways = [[[47, 343], [64, 338]], [[64, 338], [142, 546]], [[47, 344], [179, 699]], [[180, 700], [196, 692]], [[196, 692], [147, 566]], [[147, 566], [442, 461]], [[442, 461], [444, 483]], [[444, 483], [460, 482]], [[460, 482], [460, 453]], [[461, 455], [463, 533]], [[463, 533], [476, 540]], [[476, 540], [475, 452]], [[475, 452], [654, 452]], [[654, 452], [657, 545]], [[657, 545], [669, 544]], [[669, 544], [667, 475]], [[667, 475], [667, 494]], [[667, 494], [682, 493]], [[682, 493], [681, 452]], [[681, 452], [854, 450]], [[854, 450], [859, 676]], [[859, 676], [881, 678]], [[881, 678], [874, 448]], [[874, 448], [918, 444]], [[876, 464], [918, 461]], [[918, 461], [964, 461]], [[964, 461], [964, 410]], [[964, 411], [918, 411]], [[918, 411], [906, 76]], [[906, 76], [954, 76]], [[954, 76], [953, 62]], [[953, 62], [817, 61]], [[817, 61], [815, 29]], [[815, 29], [778, 33]], [[778, 33], [777, 63]], [[777, 63], [743, 63]], [[743, 63], [741, 56]], [[741, 56], [718, 57]], [[718, 57], [716, 64]], [[716, 64], [730, 66]], [[730, 66], [733, 183]], [[733, 183], [609, 226]], [[609, 226], [584, 157]], [[584, 157], [576, 150]], [[576, 150], [606, 106]], [[606, 106], [556, 70]], [[556, 70], [548, 82]], [[547, 82], [587, 113]], [[587, 113], [547, 167]], [[547, 167], [580, 192]], [[580, 191], [593, 235]], [[593, 236], [411, 300]], [[411, 300], [391, 243]], [[391, 243], [359, 224]], [[359, 225], [437, 443]], [[437, 443], [143, 546]], [[290, 495], [276, 460]], [[276, 460], [263, 466]], [[263, 466], [264, 476]], [[264, 476], [270, 476]], [[270, 476], [279, 497]], [[416, 314], [600, 247]], [[600, 247], [651, 392]], [[651, 392], [651, 431]], [[651, 431], [538, 434]], [[538, 434], [529, 411]], [[529, 411], [518, 415]], [[518, 415], [526, 434]], [[526, 433], [462, 437]], [[462, 437], [451, 412]], [[451, 412], [460, 409]], [[460, 409], [434, 335]], [[435, 334], [438, 333]], [[438, 333], [429, 310]], [[748, 81], [886, 75]], [[886, 75], [898, 430]], [[898, 430], [805, 430]], [[805, 430], [803, 372]], [[803, 372], [858, 372]], [[858, 372], [850, 76]], [[749, 81], [751, 194]], [[751, 194], [613, 244]], [[613, 244], [657, 375]], [[657, 375], [691, 374]], [[691, 374], [691, 393]], [[691, 393], [665, 395]], [[665, 395], [665, 429]], [[665, 429], [787, 429]], [[787, 429], [787, 372]], [[787, 372], [773, 372]], [[773, 372], [754, 328]], [[754, 328], [774, 322]], [[774, 322], [747, 243]], [[747, 243], [729, 249]], [[729, 249], [713, 209]], [[750, 82], [856, 369]], [[770, 370], [849, 79]], [[852, 241], [722, 233]], [[326, 625], [326, 625]], [[325, 623], [343, 679]], [[343, 679], [325, 680]], [[325, 680], [331, 703]], [[331, 703], [332, 741]], [[332, 741], [357, 740]], [[357, 740], [354, 703]], [[354, 703], [537, 699]], [[537, 699], [536, 739]], [[536, 739], [554, 739]], [[554, 739], [555, 698]], [[555, 698], [745, 695]], [[745, 695], [744, 737]], [[744, 738], [762, 736]], [[762, 736], [762, 673]], [[762, 673], [367, 680]], [[367, 680], [354, 641]], [[354, 641], [368, 640]], [[368, 640], [362, 611]], [[362, 611], [328, 624]]]

def dist(a,b):
    return np.sqrt(int(a[0] - b[0]) *int(a[0] - b[0])  + int(a[1] - b[1]) * int(a[1] - b[1]))
def rssiToDist(rssi):
    #10^((Measured Power - Instant RSSI)/10*N).
    return a * pow(2.71828,(float(rssi) * -1.0 * b)) * meterScale
    #return a * pow(((float(rssi) * -1.0)),b)  * meterScale
   # print((10 ^ ((-67 - (rssi))/10 * 3))/1000)
    #return (10 ^ int((meterRSSI - float(rssi))/10 * environmentalFactor)) * meterScale
#ser = serial.Serial('/dev/tty.usbmodem14201')

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
bg = PhotoImage(file = "YOURIMAGEHERE.png")
  
# Create Canvas
canvas = Canvas( root, width = 970,
                 height = 750)
  
canvas.pack(fill = "both", expand = True)

# Display image
canvas.create_image( 0, 0, image = bg, 
                     anchor = "nw")
for border in schoolOutline:
    canvas.create_line(border[0][0],border[0][1],border[1][0],border[1][1],fill="red",width=3) 
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
for wap in foundWaps:
    if(wap[2][0] == "7"):
       # canvas.create_circle(wap[0], wap[1], 5, fill="white", outline="red", width=5)
       pass
    elif(wap[2][1] == "4" or wap[2][1] == "6"):
        canvas.create_circle(wap[0], wap[1], 5, fill="white", outline="green", width=5)

#FOR VISUALIZATION ONLY
def showPosition(showData):
    global bssids, rssis, checkPoints
    failures = 0
    totalAvg = 0
    canvas.create_image( 0, 0, image = bg, 
                     anchor = "nw")
    start_time = time.time()
    for wap in foundWaps:
        if(wap[2][0] == "7"):
        # canvas.create_circle(wap[0], wap[1], 5, fill="white", outline="red", width=5)
            pass
        elif(wap[2][1] == "4" or wap[2][1] == "6"):
            if(showData):
                canvas.create_circle(wap[0], wap[1], 5, fill="white", outline="green", width=5)
    #Goes through every test point
    for (num, bssidPoint) in enumerate(bssids):
        #Selects the first test point
        if num == 0:
            #Creates an empty array of points
            points = []
            minBounds = []
            maxBounds = []
            
            #Defines the circular bounds for each WAP
            for (index, bssid) in enumerate(bssidPoint):
                #draws center (og predicted RSSI)
                if(showData):
                    canvas.create_circle(getWAPpos(bssidPoint[index])[0], getWAPpos(bssidPoint[index])[1], rssiToDist(rssis[num][index]), fill="", outline="red", width=3)
                #draws boundary error rssis based on pre-determined error value
                maxRadius = rssiToDist(rssis[num][index] * (1 + (rssiError / 2 / 100)))
                minRadius = rssiToDist(rssis[num][index]  * (1 - (rssiError / 2 / 100)))
                
                maxBounds.append(maxRadius)
                minBounds.append(minRadius)
            #Refreshes Screen
            #DRAWS WAP CIRCLES
            #draws center (og predicted RSSI)
            if(showData):
                canvas.create_circle(getWAPpos(bssidPoint[0])[0], getWAPpos(bssidPoint[0])[1], rssiToDist(rssis[0][0]), fill="", outline="red", width=3)
            #draws boundary error rssis based on pre-determined error value
            maxRadius = rssiToDist(rssis[0][0] * (1 + (rssiError / 2 / 100)))
            minRadius = rssiToDist(rssis[0][0]  * (1 - (rssiError / 2 / 100)))
            #canvas.create_circle(getWAPpos(bssidPoint[0])[0], getWAPpos(bssidPoint[0])[1], minRadius, fill="", outline="green", width=3)
           # canvas.create_circle(getWAPpos(bssidPoint[0])[0], getWAPpos(bssidPoint[0])[1], maxRadius, fill="", outline="green", width=3)
            #canvas.create_circle(getWAPpos(bssid)[0], getWAPpos(bssid)[1], minRadius, fill="", outline="orange", width=3)
            #canvas.create_circle(getWAPpos(bssid)[0], getWAPpos(bssid)[1], maxRadius, fill="", outline="orange", width=3)
            #Will store all of the "buffer points"
            circlePoints = []
            #Creates a bunch of filler circles in between the max and min circles. Multiplied and divided by a hundred because floats aren't allowed in a for loop in python
            radius = minRadius
            while radius < maxRadius:
                #Draws the buffer circles.
                #canvas.create_circle(getWAPpos(bssid)[0], getWAPpos(bssid)[1], radius / 100, fill="", outline="yellow", width=3)
                #Defines the spacing of the buffer points along the circle
                spacing = (rssiToDist(rssis[0][0]) * 2 * 3.14159) / 2
                #Goes through each angle degree on the circle, to draw all the point for that angle
                angle = 0
                while angle < spacing:
                    #Draws the poinnt on the buffer circle
                    x  = (radius)*math.cos(angle * (3.141592165 / 180) * (360 / spacing)) + getWAPpos(bssidPoint[0])[0]
                    y  = (radius)*math.sin(angle * (3.141592165 / 180) * (360 / spacing)) + getWAPpos(bssidPoint[0])[1]
                    #canvas.create_circle(x, y, 1, fill="blue", outline="blue", width=1)
                    isInBounds = True
                    for num in range(len(minBounds)):
                        if dist(getWAPpos(bssidPoint[num]), [x,y]) < (minBounds[num]) or dist(getWAPpos(bssidPoint[num]), [x,y]) > (maxBounds[num]):
                            isInBounds = False
                    if isInBounds:
                        circlePoints.append([x,y])

                    angle += 1
                radius += 1.2
            points.append(circlePoints)
            #for num in range(len(maxBounds)):
            #    canvas.create_circle(getWAPpos(bssidPoint[num])[0], getWAPpos(bssidPoint[num])[1], minBounds[num], fill="", outline="black", width=3)
            #    canvas.create_circle(getWAPpos(bssidPoint[num])[0], getWAPpos(bssidPoint[num])[1], maxBounds[num], fill="", outline="black", width=3)
            for circle in points:
                for point in circle:
                    if(showData):
                        pass
                        #canvas.create_circle(point[0], point[1], 1, fill="green", outline="green", width=1)
            return points
# Define a function that takes a list of points and a threshold value as input
def isolate_groups(points, threshold):
  
  # Create an empty list to store the isolated groups of points
  groups = []
  
  # Loop through each point in the list
  for point in points:
    
    # Create a flag variable to keep track of whether the point has been added to a group
    added = False
    
    # Loop through each group in the list
    for group in groups:
      
      # Calculate the distance between the current point and the centroid of the current group
      dist = calculate_distance(point, calculate_centroid(group))
      
      # If the distance is less than or equal to the threshold, add the point to the group
      if dist <= threshold:
        group.append(point)
        added = True
        break
    
    # If the point has not been added to a group, create a new group with the point as its only member
    if not added:
      groups.append([point])
  
  # Return the list of isolated groups of points
  return groups

# Define a function to calculate the distance between two points
def calculate_distance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Define a function to calculate the centroid of a group of points
def calculate_centroid(group):
  x_sum = 0
  y_sum = 0
  for point in group:
    x, y = point
    x_sum += x
    y_sum += y
  return (x_sum / len(group), y_sum / len(group))






#END VISUALIZATION CODE
p = 0
#showPosition()
#updateStudentPosition("224288","blue")
#canvas.create_line(0,0,500,500,fill="green",width=2) 
def motion(event):
    global mouseX, mouseY
    x, y = event.x, event.y
    if(x > 0 and x < 970 and y > 0 and y < 750):
        mouseX = x
        mouseY = y
def leftclick(event):
    pass
def processData(line, emergency):
    global bssids, rssis, a, b, pastPoints, roomBSSIDs,roomBounds,roomNums, roomPositions, schoolOutline, schoolBorders, testArrays, testArrayNumber, pastX, pastY, pastDist
   # canvas.create_circle(mouseX, mouseY, 5, fill="", outline="blue", width=3)
    #print("Clicked")
    #line = ser.readline()   # read a '\n' terminated line
   # line = "-" + str(random.randint(60,90)) + ",D4:F9:8D:70:F1:2D -" + str(random.randint(60,90)) +  ",D4:F9:8D:70:F1:7B"
    #line = testArrays[testArrayNumber]
    #testArrayNumber += 1
    #print(line)
    #data = line.decode().rstrip()
    data = line.rstrip()
    #print(data)
    waps = data.split(" ")
    rssis2 = []
    bssids2 = []
    for wap in waps:
        rssis2.append(int(wap.split(",")[0]))
        bssids2.append(wap.split(",")[1])
    #showMUXPosition(bssids,rssis)
    #print(bssids2, rssis2)
    #print()
    #print(rssiToDist(-90))
    bssids[0] = bssids2
    rssis[0] = rssis2
    #Calculates the closest access point in the event that no points are found
    lowestRssi = rssis2[0]
    lowestbssid = bssids2[0]
    for (num, rssi) in enumerate(rssis2):
        #Remember RSSI is inverse, so higher is a lower distance
        if rssi > lowestRssi:
            lowestRssi = rssi
            lowestbssid = bssids2[num]
    #Gets the points calculated for the currently scanned data
    currPoints = showPosition(True)
    #This will store the resulting data after filtering
    actualPoints = []
    #Flattens the current points array
    flattenedCurrentPoints = []
    for row in currPoints:
        for point in row:
            flattenedCurrentPoints.append(point)
    currPoints = flattenedCurrentPoints
    #If we have a set of previous points,
    if len(pastPoints) > 0:
        #If we have currelty scanned data
        if len(currPoints) > 0:
            #Loop through every scanned data point
            for point in currPoints:
                if dist([round(point[0], 2),round(point[1], 2)], [pastX, pastY]) < pastDist:
                    #Add that new point to the filtered point list
                    actualPoints.append([round(point[0], 2),round(point[1], 2)])
        #If we do not have any currently scanned data
        if len(currPoints) == 0:
            #We are in a classroom
            #Find the room number's position based on the closest wap and set it to the filtered result
            for (num,waps) in enumerate(roomBSSIDs):
                if lowestbssid in waps:
                    actualPoints = [roomPositions[num]]
    #If we do not have any resulting points
    if len(actualPoints) == 0:
        #If we have current points that are nowhere near the past points, set the filtered points to the new points
        if len(currPoints) > 0:
            for point in currPoints:
                actualPoints.append(point)
        else:
            #If we have no current points, no filtered points, and no past points, do the same classroom assumption technique
            for (num,waps) in enumerate(roomBSSIDs):
                if lowestbssid in waps:
                    actualPoints = [roomPositions[num]]
    else:
        pastPoints = []
    #Reset the past points array with current points
    for point in currPoints:
        pastPoints.append([round(point[0], 2),round(point[1], 2)])
    xAvg = 0
    yAvg = 0
    
    #If the lowest RSSI is below 60, assume the student is in a classroom, and exclude all values outside of it.
    #Does the vice-versa as well

    tempActualPoints = []
    if(len(actualPoints) > 3):
        for point in actualPoints:
            bound = 0
            for(num, abound) in enumerate(roomBSSIDs):
                if(lowestbssid in abound):
                    bound = roomBounds[num]
            if(lowestRssi * -1 <= 60):
                if((bound[0] <= point[0] and bound[2] >= point[0]) and (bound[1] <= point[1] and bound[3] >= point[1])):
                    tempActualPoints.append(point)
                    canvas.create_circle(point[0], point[1], 1, fill="purple", outline="", width=2)
            else:
                inBounds = False
                for(num, abound) in enumerate(roomBSSIDs):
                    bound = roomBounds[num]
                    if((bound[0] <= point[0] and bound[2] >= point[0]) and (bound[1] <= point[1] and bound[3] >= point[1])):
                        inBounds = True
                if not inBounds:
                    tempActualPoints.append(point)
                    canvas.create_circle(point[0], point[1], 1, fill="purple", outline="", width=2)
                
                        
        actualPoints = tempActualPoints
    #If we do not have any resulting points
    if len(actualPoints) <= 1:
        #Flattens the current points array
        flattenedCurrentPoints = []
        for row in currPoints:
            for point in row:
                flattenedCurrentPoints.append(point)
        #If we have current points that are nowhere near the past points, set the filtered points to the new points
        if len(flattenedCurrentPoints) > 0:
            for point in flattenedCurrentPoints:
                actualPoints.append(point)
        else:
            #If we have no current points, no filtered points, and no past points, do the same classroom assumption technique
            for (num,waps) in enumerate(roomBSSIDs):
                if lowestbssid in waps:
                    actualPoints = [roomPositions[num]]
    #Determines groups of points and removes the smallest group
    pointsLists = []
    circleRad = 2.0 * meterScale
    #PSUEDO CODE
    #Loop through each point
        #create tempList
        #Loop through all other points
            #If dist between OG point and new point < circleRad, add to temp list
        #If pointsLists length is 0 add tempList to pointsList
        #If not, loop through each list in pointsLists
            #if a point in tempList is inside of the looping list, add all NON DUPLICATES to the list in pointsLists
                #break loop
    #Go through each point list
        #Go through all other point lists
            #If there is a new point list that has a single point in the OG point list,
                #Combine two lists, removing duplicates
    #We now have lists of grouped points
    #Calculates a circle that encapsulates all poinst based on a circle based on 2 endpoints
    results = getCenterAndError(actualPoints)
    xAvg = results[0]
    yAvg = results[1]
    farthestDist = results[2]
    pastX = xAvg
    pastY = yAvg
    pastDist = farthestDist
    #Draws the circle of possibility
    #print(isInDanger(xAvg, yAvg, farthestDist, 0))
    canvas.create_circle(xAvg, yAvg, farthestDist, fill="", outline="green", width=4)
    #print(round(farthestDist / meterScale, 2))
    print(xAvg, yAvg, farthestDist, isInDanger(xAvg, yAvg, farthestDist, emergency))
    #sessionBSSIDS.append(bssids)
    #sessionRSSIS.append(rssis)
    #sessionPoints.append([int(mouseX), int(mouseY)])
    #canvas.create_circle(mouseX, mouseY, 5, fill="", outline="green", width=3)
   

def getCenterAndError(list):
    #print(list)
    try:
        if(len(list) > 1):
            #Calculates a circle that encapsulates all poinst based on a circle based on 2 endpoints
            xAvg = 0
            yAvg = 0    
            minPoint = [100000,0]
            maxPoint = [0,0]         
            #Visually display the resutling points and calculates the middle of all points
            for point in list:
                if point[0] < minPoint[0]:
                    minPoint = point
                if point[0] > maxPoint[0]:
                    maxPoint = point
                #canvas.create_circle(point[0], point[1], 2, fill="blue", outline="blue", width=1)
            farthestDist = dist(minPoint, maxPoint) / 2
                #canvas.create_circle(point[0], point[1], 2, fill="blue", outline="blue", width=1)
            xAvg = (minPoint[0] + maxPoint[0]) / 2
            yAvg = (minPoint[1] + maxPoint[1]) / 2
                    
            #canvas.create_circle(farthestPoint[0], farthestPoint[1], 1, fill="", outline="red", width=10)
            if(farthestDist == 0):
                farthestDist = 2.0 * meterScale
            return [xAvg, yAvg, farthestDist]
        else:
            return [list[0][0], list[0][1], 2.0 * meterScale]
    except:
        print("ERROR")
        return [list[0][0], list[0][1], 2.0 * meterScale]
def isInDanger(x,y,rad,state):
    #state numbers
    #0 - lockout
    #1 - lockdown
    #-1 - no emergency
    if(state != -1):
        if(x != 0 and y != 0):
            #Basically goes through each border that outlines the school and determines if the circle intersects the line segment
            #Y values are multiplied by negative 1 because y is inverse
            #Creates a line segment because by creating a xMin and xMax and iterating between each of them.
            outlines = schoolOutline
            if(state != 0):
                outlines = schoolHallways
            for (num,border) in enumerate(outlines):
                    xMax = x + rad
                    xMin = x - rad
                    
                    x1 = border[0][0]
                    y1 = (750 - border[0][1])
                    x2 = border[1][0]
                    y2 = (750 - border[1][1])
                    if(x1 - x2 != 0):
                        m = (y1 - y2) / (x1 - x2)
                        b = (y1) - m * x1
                        interval = xMin
                        while interval <= xMax:
                            if((x1 < interval and interval < x2) or (x2 < interval and interval < x1)):
                                if(dist([x,(750 - y)], [interval, (interval * m + b)]) <= rad):
                                    return True
                            interval += 0.5
            return False
        return False
    return False

def pointInList(point, list):
    lowestDist = 1000000
    for row in list:
        for dot in row:
            if dist(point,dot) < 10:
                return -1
            elif dist(point, dot) < lowestDist:
                lowestDist = dist(point, dot)
    return lowestDist
def finish(event):
    print(sessionPoints)
    print(sessionBSSIDS)
    print(sessionRSSIS)
#root.bind('<Motion>', motion)
#root.bind("<Button-1>", leftclick)
#root.bind("<Return>", finish)
#showPosition()

if(len(sys.argv) == 3):
    #try:
    start = time.time()
    processData(str(sys.argv[1]), int(sys.argv[2]))
    stop = time.time()
    print(stop - start)
        #root.mainloop()
    #except:
        #print("ERROR")
else:
    print("Incorrect arguments passed. Pass a string of the WAP data in the format: RSSI,BSSID RSSI,BSSID... AND emergency status")


    
