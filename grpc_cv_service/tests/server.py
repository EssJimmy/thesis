import os
import sys
import grpc
import logging
from concurrent import futures

DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(DIR, "../.."))
sys.path.insert(0, PARENT_DIR)

from grpc_cv_service.depth_camera_service import depth_camera_pb2_grpc as d_grpc

class RobotVision(d_grpc.DepthCameraServicer):

    def SendDepthImage(self, request, context):
        print(f"Received depth data: {request.depth_values}mm at ({request.x_coord}, {request.y_coord})")
        # TODO: Implement robot logic here
        from google.protobuf import empty_pb2
        return empty_pb2.Empty()
    
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