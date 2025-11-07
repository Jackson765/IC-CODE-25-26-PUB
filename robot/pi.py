import asyncio
import json
import math
import os
import signal
import subprocess
import sys
import time
import threading
import pigpio
import socket

from readonly import RobotBase, MOTORS

OPERATOR_IP = "192.168.50.150" # your laptop/pc ip address on IC2026 Network
OPERATOR_PORT = 5600 # the port for video streaming 
TEAM_ID = 14 # Your team ID

PI_IP = "192.168.50.5" # Your pi IP
PI_PORT = 5005  # 
pivotID1 = 0
pivotID2 = 0

MIN_DUTY_FLOOR = 30
PURE_DC_THRESHOLD = 80

### Bind Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((PI_IP, PI_PORT))
### Input Receiving Loop
def input_loop():
    input_thread = threading.Thread(target=input_loop, daemon=True)
inputQ = []
def get_input():
    while True:
        try:
            data, addr = sock.recvfrom(1024) 
            msg = json.loads(data.decode('utf-8'))
            inputQ.append(msg)
            print(f"[Received from {addr}] {msg}")
        except Exception as e:
            print("[Receiver Error]", e)
        # Tank Drive
        left = 0
        if keyboard.is_pressed("w"):
            left = 1
        elif keyboard.is_pressed("s"):
            left = 1
        right = 0
        if keyboard.is_pressed("up"):
            right = 1
        if keyboard.is_pressed("down"):
            right = 1
        pivot1 = 0
        if keyboard.is_pressed("a"):
            pivot1 = 1
        if keyboard.is_pressed("d"):
            pivot1 = 1
        pivot2 = 0
        if keyboard.is_pressed("w"):
            pivot2 = 1
        if keyboard.is_pressed("s"):
            pivot2 = 1

        payload = {
            "Left": float(left),
            "Right": float(right),
            "Pivot1": float(pivot1),
            "Pivot2": float(pivot2)
        }
        try:
            sock.sendto(json.dumps(payload).encode("utf-8"), (PI_IP,PI_PORT)) # send our json to our Pi at the appropriate IP an Port
            sock.settimeout(0.001) # set a timoout for the socket
            try:
                data, addr = sock.recvfrom(1024) # try to get a response from the socket
                response = json.loads(data.decode("utf-8"))
                
                # Debug print for self-hits
                if response.get("is_self_hit", False):
                    print(f"[GUI] Self-hit detected in response: {response}")
                    
            except (socket.timeout, json.JSONDecodeError):
                pass
            finally:
                sock.settimeout(None)
        except Exception as e:
            print(f"UDP error: {e}") # catch and report the error
def apply_motor(name, norm):
    """Apply motor control with PWM"""
    norm = clamp(norm, -1.0, 1.0) * DIR_OFFSET[name]
    if (name == "Pivot1"):
        pins = pivotID1
    elif (name == "Pivot2"):
        pins = pivotID2
    else:
        pins = MOTORS[name]
    
    if abs(norm) < 1e-3:
        pi.set_PWM_dutycycle(pins["EN"], 0)
        pi.write(pins["IN1"], 0)
        pi.write(pins["IN2"], 0)
        return
   
    forward = norm > 0
    pi.write(pins["IN1"], 1 if forward else 0)
    pi.write(pins["IN2"], 0 if forward else 1)
   
    pct = int(abs(norm) * 100)
    if pct >= PURE_DC_THRESHOLD:
        pi.write(pins["EN"], 1)
    else:
        pct = max(MIN_DUTY_FLOOR, pct)
        duty = pct * 255 // 100
        pi.set_PWM_dutycycle(pins["EN"], duty)


class Robot(RobotBase):
    ### Bind Socket

    def __init__(self, team_id):
        super().__init__(team_id)
        ### Initialization/Start Up
        pass

        ### Socket Receive Thread

    def run(self):
        try:
            while True:
                pass
        except Exception as e:
            pass
        finally:
            self.cleanup()

    def stream(self):
        pass

    def set_motor(self):
        apply_motor(self)

    def cleanup(self):
        pass

    def input_loop():
        input_thread = threading.Thread(target=input_loop, daemon=True)

    def tank_drive(self):
        if len(inputQ) > 0:
            inputJSON = inputQ.pop(0)
            self.set_motor("FL", inputJSON["Left"])
            self.set_motor("BL", inputJSON["Left"])
            self.set_motor("FR", inputJSON["Right"])
            self.set_motor("BR", inputJSON["Right"])

            self.set_motor("Pivot1", inputJSON["Pivot1"])
            self.set_motor("Pivot1", inputJSON["Pivot1"])
            self.set_motor("Pivot2", inputJSON["Pivot2"])
            self.set_motor("Pivot2", inputJSON["Pivot2"])

if __name__ == "__main__":
    team_id = 14  # your team id here

    robot = Robot(team_id)
    try:
        robot.run()
    except KeyboardInterrupt:
        print("\n[Shutdown] Received interrupt")
    except Exception as e:
        print(f"[Error] {e}")
    finally:
        robot.cleanup()