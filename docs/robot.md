```python
import os
import sys
import time
import grpc
import logging
from typing import Any
from datetime import datetime
from concurrent import futures

DIR = os.path.dirname(os.path.abspath(__file__))

# Add parent directory to path so grpc_cv_service package can be found
PARENT_DIR = os.path.abspath(os.path.join(DIR, ".."))
sys.path.insert(0, PARENT_DIR)

from xarm.wrapper import XArmAPI
from grpc_cv_service.depth_camera_service import depth_camera_pb2_grpc as d_grpc

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

ip = load_robot_config()
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.clean_error()
arm.set_mode(0)
arm.set_state(0)
time.sleep(0.2)
arm.move_gohome(wait=True)

class RobotVision(d_grpc.DepthCameraServicer):

    def SendDepthImage(self, request, context):
        print(f"""{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}: Received depth data: {request.depth_values}mm at ({request.x_coord}, {request.y_coord})""")
        arm.set_position(y=request.y_coord, z=request.x_coord, speed=100, wait=True)
        print(arm.get_position())
        from google.protobuf import empty_pb2
        return empty_pb2.Empty()
        

def serve():
    arm.set_servo_angle(angle=[0, 0, 0, 0, 90, 0], speed=50, wait=True)
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

```