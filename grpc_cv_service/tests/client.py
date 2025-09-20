import os
import sys
import grpc

DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(DIR, "../.."))
sys.path.insert(0, PARENT_DIR)


from grpc_cv_service.depth_camera_service import depth_camera_pb2_grpc as d_grpc
from grpc_cv_service.depth_camera_service import depth_camera_pb2 as d_pb2

def main() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        print("Connected to server")
        stub = d_grpc.DepthCameraStub(channel)

        for i in range(1, 11):
            depth_request = d_pb2.DepthRequest(
                        depth_values=float(i),
                        x_coord=int(i*10),
                        y_coord=int(i*5)
                    )
            stub.SendDepthImage(depth_request)

if __name__ == '__main__':
    main()