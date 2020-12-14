import time
import serial, sys, collections


def parceLine(a):
    i0 = 2
    i1 = a.find('\t')
    can_id = int(a[i0:i1],16)
   
    can_data = []

    while(a.find('\t', i1+1) > 0):
        i0 = a.find('\t', i1) + 1
        i1 = a.find('\t', i0)
        can_data.append(int(a[i0:i1],16))

    return can_id, can_data

def printData(a):
    global printTime
    if(time.time() - printTime > 0.25):
        printTime = time.time()
        a = collections.OrderedDict(sorted(a.items()))
        pt = "\n" *25
        print(pt)
        for i in a:
            tc = 1
            can_id = i
            can_data = a[i]
            print(hex(can_id) + "\t", end = '')
            for dat in can_data:
                print(hex(dat)[2:] + "\t", end = '')
                tc = tc + 1

            while(tc < 10):
                print('\t', end = "")
                tc = tc + 1
           
            print("Period:"+ str(round((times[can_id] - prevtime[can_id])*1000, 2)))
            prevtime[can_id] = times[can_id]


data = {}
times = {}
prevtime = {}
printTime = time.time()

ser = serial.Serial('COM3', 115200, timeout=0)
count = 0
while 1:
    if ser.inWaiting()>90:
        a = ser.readline().decode("utf-8")
        count = count + 1
        if count > 10:
            can_id, can_data = parceLine(a)
            data[can_id] = can_data
            times[can_id] = time.time()
            if can_id not in prevtime.items():
                prevtime[can_id] = 0
            printData(data)
   
ser.close()