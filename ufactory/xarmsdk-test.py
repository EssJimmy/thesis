import os
import time
import sys
import numpy as np
import time


DIR = os.path.dirname(__file__) 
SDK_DIR = os.path.join(DIR, 'xArm-Python-SDK/')
sys.path.append(SDK_DIR)

REALSENSE_DIR = os.path.abspath(os.path.join(DIR, "../realsense"))
sys.path.insert(1, REALSENSE_DIR)

from xarm.wrapper import XArmAPI
from realsense.camera_system import get_streaming_models

def load_robot_config():
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    else:
        try:
            from configparser import ConfigParser
            parser = ConfigParser()
            parser.read(os.path.join(DIR, "robot.conf"))
            ip = parser.get('xArm', 'ip')
        except:
            ip = input('Please input the xArm ip address:')
            if not ip:
                print('input error, exit')
                sys.exit(1)

    return ip

def __callback_report_location(item):
    print('location report:', item)

def main() -> None:
    ip = load_robot_config()
    arm = XArmAPI(ip)
    arm.register_report_location_callback(callback=__callback_report_location)

    arm.motion_enable(enable=True)
    arm.clean_error()
    arm.set_mode(0)
    arm.set_state(state=0)
    time.sleep(0.2)
    arm.move_gohome(wait=True)
    

    #arm.set_servo_angle(angle=[0, 0, 0, 0, 90, 0], speed=50, wait=True)
    """i = 0
    found = False
    while not found:
        arm.set_servo_angle(angle=[45*i, 0, 0, 0, 90, 0], speed=50, wait=True)
        time.sleep(3)

        i += 1
        if i == 8:
            found = True

    arm.move_gohome(wait=True)"""
    arm.disconnect()


if __name__ == "__main__":
    main()
