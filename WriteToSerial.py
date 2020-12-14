import serial
ser = serial.Serial('COM21', 115200, timeout=0)
ser.write("0x4315\t3\t2\t0\t0\t8F\t1D\t1F\n".encode("utf-8"))