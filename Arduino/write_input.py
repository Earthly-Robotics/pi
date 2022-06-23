import serial,time
if __name__ == '__main__':
    
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    cmd=input("Enter command : ")
                    arduino.write(cmd.encode())
                    time.sleep(0.1) #wait for arduino to answer
                    while arduino.in_waiting == 0:
                        #print(arduino.in_waiting)
                        pass
                    if  arduino.in_waiting > 0:
                        answer=arduino.readline()
                        print(answer)
                        arduino.reset_input_buffer() #remove data after reading
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")