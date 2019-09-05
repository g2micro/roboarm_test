#!/usr/local/bin/python3

# MIT License
# See LICENSE file
# Copyright (c) 2019 g2micro

import serial
import sys
import time

# Change this to the serial port on which the servo board is connected.
serial_port = '/dev/tty.usbserial-AM4FN7PB'


def send(cmd):
    b=bytes(cmd, encoding="utf-8")
    ser.write(b)  # write a string
    print (cmd)
    ser.flush()
    ser.read(16)

def menu():
    cmd_head_tilt_right="#4D200T1000\r\n"
    cmd_head_tilt_left="#4D-200T1000\r\n"
    cmd_head_straight="#4D0T1000\r\n"

    cmd_base_0="#0D0T2000\r\n"
    cmd_base_90="#0D900T2000\r\n"

    cmd_base_90_slow= "#0D900T10000\r\n"
    cmd_base_m90_slow="#0D-900T10000\r\n"

    cmd_elbow_flat="#2D900T2000\r\n"
    cmd_elbow_low="#2D450T2000\r\n"
    cmd_elbow_normal="#2D0T2000\r\n"
    cmd_elbow_high="#2D-900T2000\r\n"
    cmd_elbow_forward="#2D-450T2000\r\n"
    cmd_elbow_lforward="#2D-900T2000\r\n"

    cmd_shoulder_flat="#1D900T2000\r\n"
    cmd_shoulder_low="#1D675T2000\r\n"
    cmd_shoulder_normal="#1D450T2000\r\n"
    cmd_shoulder_high="#1D0T2000\r\n"
    cmd_shoulder_forward="#1D-450T2000\r\n"
    cmd_shoulder_lforward="#1D-900T2000\r\n"

    cmd_wrist_flat = "#3D0T2000\r\n"
    cmd_wrist_low = "#3D-225T2000\r\n"
    cmd_wrist_normal = "#3D-450T2000\r\n"
    cmd_wrist_high = "#3D-900T2000\r\n"

    while (True):
        print("1: Return to rest position")
        print("2: Return to low position")
        print("3: Return to normal position")
        print("4: Return to high position")
        print("5: Search - let base continuously swing -90 to +90 and back")
        print("6: Led Set - set all LEDs to specified colour.")
        print("7: Head Tilt")
        print("8: Rotate Base")
        print("9: Reach Forward")
        print("10: Reach Low Forward")
        print("11: Configure Led Blink")
        print("12: Reset All")

        input = sys.stdin.readline().rstrip()

        if (input == "1"):
            cmd = cmd_elbow_flat + cmd_shoulder_flat + cmd_base_0 + cmd_wrist_flat + cmd_head_straight
            send(cmd)

        if (input == "2"):
            cmd = cmd_elbow_low + cmd_shoulder_low + cmd_base_0 + cmd_wrist_low + cmd_head_straight
            send(cmd)

        elif (input == "3"):
            cmd = cmd_elbow_normal + cmd_shoulder_normal + cmd_base_90 + cmd_wrist_normal        
            send(cmd)

        elif (input == "4"):
            cmd = cmd_elbow_high + cmd_shoulder_high + cmd_base_90 + cmd_wrist_high        
            send(cmd)

        elif (input == "5"):
            while (True):
                cmd = cmd_base_m90_slow
                send(cmd)
                time.sleep(10)
                cmd = cmd_base_90_slow
                send(cmd)
                time.sleep(10)

        elif (input == "6"):
            print("Set the colour: 0 - off, 1- red, 2 - green, 3 - blue, 4 - ?, 5 - cyan, 6 - magenta, 7 - ?")
            input = sys.stdin.readline().rstrip()
            cmd="#254LED" + input + "\r\n"            
            send(cmd)

        elif (input == "7"):
            print("Head left, right or normal [l,r,n]?")
            cmd = cmd_head_straight
            input = sys.stdin.readline().rstrip()
            if (input == 'l' or input == 'L'):
                cmd = cmd_head_tilt_left
            elif (input == 'r' or input == 'R'):
                cmd = cmd_head_tilt_right
            send(cmd)

        elif (input == "8"):
            print("Rotate base to ? deg")
            input = sys.stdin.readline().rstrip()
            cmd="#0D" + input + "0T2000\r\n"            
            send(cmd)

        elif (input == "9"):
            cmd =  cmd_wrist_flat + cmd_elbow_forward + cmd_shoulder_forward
            send(cmd)

        elif (input == "10"):
            cmd =  cmd_wrist_flat + cmd_elbow_lforward + cmd_shoulder_lforward
            send(cmd)

        elif (input == "11"):
            print("Configure Led Blink on top servo: Blink while: 1=Limp; 2=Holding; 4=Accel; 8=Decel; 16=Free 32=Travel;")
            input = sys.stdin.readline().rstrip()
            cmd="#4CLBD" + input + "\r\n"            
            send(cmd)

        elif (input == "12"):
            send("#254RESET\r\n")

ser = serial.Serial(port=serial_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)  # open serial port
print(ser.name, ser.is_open, ser.baudrate)         # check which port was really used
menu()
