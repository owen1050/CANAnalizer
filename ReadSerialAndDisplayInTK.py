import time, serial, sys, collections
import tkinter as tk

class App():
    def __init__(self):
        self.tkG = tk
        self.root = tk.Tk()
        self.root.geometry("500x500")
        
        self.data = {}
        self.times = {}
        self.prevtime = {}
        self.printTime = time.time()
        self.ser = serial.Serial('COM20', 115200, timeout=0)
        self.count = 0

        self.initLabels()
        self.update()
        self.root.mainloop()

    def initLabels(self):
        numberOfLabels = 30;
        labelInc = 1 / numberOfLabels
        xPos = 0.1
        self.labels = []
        for i in range(numberOfLabels):
            self.labels.append([])
            for j in range(7):
                self.labels[i].append(tk.Label(text=""))
                self.labels[i][j].place(relx = xPos*j, rely = labelInc*(i), anchor = 'nw')
        


    def update(self):
        
        if self.ser.inWaiting()>60:
            a = self.ser.readline().decode("utf-8")
            self.count = self.count + 1
            if self.count > -1:
                can_id, can_data = self.parceLine(a)
                print(can_id,can_data)
                self.data[can_id] = can_data
                self.times[can_id] = time.time()
                if can_id not in self.prevtime.items():
                    self.prevtime[can_id] = 0

        self.data = collections.OrderedDict(sorted(self.data.items()))
        c = 0
        for i in self.data:
            temp = str(i) + str(self.data[i])
            self.labels[c][0].configure(text = str(hex(i)))
            for j in range(6):
                self.labels[c][j+1].configure(text = hex(self.data[i][j]))

            c = c + 1

        self.root.after(100, self.update)

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