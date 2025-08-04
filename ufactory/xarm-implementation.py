import os
import time
import sys
import time
import grpc
from typing import Any

found = False

DIR = os.path.dirname(__file__) 
SDK_DIR = os.path.join(DIR, 'xArm-Python-SDK/')
sys.path.append(SDK_DIR)

REALSENSE_DIR = os.path.abspath(os.path.join(DIR, "../realsense"))
sys.path.append(REALSENSE_DIR)

GRPC_DIR = os.path.abspath(os.path.join(DIR, "../grpc"))
sys.path.append(GRPC_DIR)

from xarm.wrapper import XArmAPI
from realsense.normal_camera import get_cam_stream_model
from grpc_cv_service.normal_camera_service import normal_camera_pb2_grpc as n_grpc
from grpc_cv_service.normal_camera_service import normal_camera_pb2 as n_pb2
from grpc_cv_service.depth_camera_service import depth_camera_pb2_grpc as d_grpc
from grpc_cv_service.depth_camera_service import depth_camera_pb2 as d_pb2

def __callback_report_location(item):
    print('location report:', item)

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

def object_not_in_main_camera(arm: Any, channel: grpc.Channel) -> None:    
    arm.move_gohome(wait=True)
    arm.set_servo_angle(angle=[0, 0, 0, 0, 90, 0], speed=50, wait=True)
    i = 0    
    
    n_stub = n_grpc.NormalCameraStub(channel)
    d_stub = d_grpc.DepthCameraStub(channel)
    if n_stub.ObjectDetection(n_pb2.ObjectDetectionRequest(camera_id=0)):
        while not found:
            arm.set_servo_angle(angle=[45*i, 0, 0, 0, 90, 0], speed=50, wait=True)
            time.sleep(3)
            
            found = d_stub.ObjectDetection(d_pb2.ObjectDetectionRequest())
            i += 1
            if i == 8:
                break

    arm.move_gohome(wait=True)

def connect_to_robot() -> Any|None:
    ip = load_robot_config()
    try:
        arm = XArmAPI(ip)
        arm.register_report_location_callback(callback=__callback_report_location)
        return arm
    except:
        return None


if __name__ == "__main__":
    arm = connect_to_robot()
    if arm:
        object_not_in_main_camera(arm)
