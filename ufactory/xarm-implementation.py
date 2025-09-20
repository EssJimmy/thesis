import os
import sys
import time
import grpc
import logging
from typing import Any
from datetime import datetime
from concurrent import futures

found = False

DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path so grpc_cv_service package can be found
PARENT_DIR = os.path.abspath(os.path.join(DIR, ".."))
sys.path.insert(0, PARENT_DIR)

from xarm.wrapper import XArmAPI
from grpc_cv_service.depth_camera_service import depth_camera_pb2_grpc as d_grpc

class RobotVision(d_grpc.DepthCameraServicer):

    def SendDepthImage(self, request, context):
        print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}: Received depth data: {request.depth_values}mm at ({request.x_coord}, {request.y_coord})""")
        # TODO: Implement robot logic here
        from google.protobuf import empty_pb2
        return empty_pb2.Empty()
        


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

"""
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
"""

def connect_to_robot() -> Any|None:
    ip = load_robot_config()
    try:
        arm = XArmAPI(ip)
        arm.register_report_location_callback(callback=__callback_report_location)
        return arm
    except:
        return None


def serve():
    port = "50051"    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    d_grpc.add_DepthCameraServicer_to_server(RobotVision(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    """
    arm = connect_to_robot()
    if arm:
        object_not_in_main_camera(arm)
    """
