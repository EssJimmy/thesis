import depth_camera_pb2
import depth_camera_pb2_grpc
import grpc
import logging
from concurrent import futures

class TestServer(depth_camera_pb2_grpc.DepthCameraServicer):

    def ObjectDetection(self, request, context):
        return depth_camera_pb2.ObjectDetectionResponse(success=True)

    def GetDepthImage(self, request, context):
        return depth_camera_pb2.DepthResponse(depth_values=12.2, timestamp="test_timestamp", x_coord=12, y_coord=12)
    

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    depth_camera_pb2_grpc.add_DepthCameraServicer_to_server(TestServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("Server started, listening on port " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()