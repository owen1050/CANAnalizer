import time, serial, sys, collections
import tkinter as tk

class App():
    def __init__(self):
        self.tkG = tk
        self.root = tk.Tk()
        self.root.geometry("900x500")
        
        self.data = {}
        self.times = {}
        self.prevtime = {}
        self.printTime = time.time()
        self.ser = serial.Serial('COM20', 115200, timeout=0)
        self.count = 0

        self.outputMode = 0 #0 - binary; 1 - hex; 2 - decimal

        self.initLabels()
        self.update()
        self.root.mainloop()

    def initLabels(self):
        numberOfLabels = 30;
        labelInc = 1 / numberOfLabels
        xPos = 0.08
        self.labels = []
        for i in range(numberOfLabels):
            self.labels.append([])
            for j in range(9):
                self.labels[i].append(tk.Label(text=""))
                self.labels[i][j].place(relx = xPos*j, rely = labelInc*(i), anchor = 'nw')

    def update(self):
        
        while self.ser.inWaiting()>60:
            a = self.ser.readline().decode("utf-8")
            if("0x" in a):
                #print(a)
                pass
            self.count = self.count + 1
            
            if self.count > 2 and "0x" in a:
                can_id, can_data = self.parceLine(a)
                if can_id in self.data:
                    for i in range(len(can_data)):
                        if(self.data[can_id][i] == can_data[i]):
                            self.data[can_id][i] = can_data[i]
                        else:
                            self.data[can_id][i] = can_data[i]
                            self.times[can_id][i] = time.time()
                else:
                    print("New id " + str(can_id) + " data " + str(can_data))
                    while(len(can_data) < 8):
                        can_data.append(0)
                    self.data[can_id] = can_data
                    self.times[can_id] = [time.time()]*8
                #print( hex(can_id), self.data[can_id], self.times[can_id])
            

        self.data = collections.OrderedDict(sorted(self.data.items()))
        c = 0
        for i in self.data:
            temp = str(i) + str(self.data[i])
            self.labels[c][0].configure(text = str(hex(i)))
            c2=1
            for j in self.data[i]:
                if time.time() - self.times[i][c2-1] < 1:
                    self.labels[c][c2].configure(text = self.formatData(j), bg = 'green')
                else:
                    self.labels[c][c2].configure(text = self.formatData(j), bg = 'white')
                c2=c2+1

            c = c + 1

        self.root.after(100, self.update)

    def formatData(self, d):
        if(self.outputMode == 0):
            return format(d, '#010b')
        if(self.outputMode == 1):
            return hex(d)
        if(self.outputMode == 2):
            return d
        return 0

    def parceLine(self, a):
        
        i0 = 2
        i1 = a.find('\t')
        can_id = int(a[i0:i1],16)
       
        can_data = []
        while(a.find('\t', i1+1) > 0):
            i0 = a.find('\t', i1) + 1
            i1 = a.find('\t', i0)
            can_data.append(int(a[i0:i1],16))

        return can_id, can_data

app=App()