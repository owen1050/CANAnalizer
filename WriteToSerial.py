import serial, time
ser = serial.Serial('COM21', 115200, timeout=0)

f = open("testData.txt")
d = f.read()
f.close()


c = 0
while c < 17500:
    l = d[c]
    ser.write(l.encode("utf-8"))
    if c % 100 == 0:
        time.sleep(0.01)
        print(c)
    c = c + 1
    if(c > 17000):
        c = 0
