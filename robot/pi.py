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

from readonly import RobotBase, MOTORS

OPERATOR_IP = "192.168.50.150" # your laptop/pc ip address on IC2026 Network
OPERATOR_PORT = 5600 # the port for video streaming 
TEAM_ID = 14 # Your team ID

PI_IP = "192.168.50.5" # Your pi IP
PI_PORT = 5005  # 

MIN_DUTY_FLOOR = 30
PURE_DC_THRESHOLD = 80

### Bind Socket

### Input Receiving Loop

class Robot(RobotBase):
    ### Bind Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((PI_IP, PI_PORT))

    ### Input Receiving Loop
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
        pass

    def cleanup(self):
        pass
    def input_loop():
        input_thread = threading.Thread(target=input_loop, daemon=True)

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