import logging
import grpc
import depth_camera_pb2
import depth_camera_pb2_grpc

def run():
    print("Will try to connect to the server...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = depth_camera_pb2_grpc.DepthCameraStub(channel)
        print("Connected to the server.")
        response = stub.ObjectDetection(depth_camera_pb2.ObjectDetectionRequest())
        print("ObjectDetection response: ", response)

        response = stub.GetDepthImage(depth_camera_pb2.DepthRequest())
        print("GetDepthImage response: ", response)



if __name__ == "__main__":
    logging.basicConfig()
    run()
