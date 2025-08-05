import cv2 as cv
import os
import sys
import grpc
import logging
from concurrent import futures
from datetime import datetime
from ultralytics import YOLO

DIR = os.path.dirname(__file__)
GRPC_DIR = os.path.abspath(os.path.join(DIR, "../grpc_cv_service"))
sys.path.append(GRPC_DIR)

import grpc_cv_service.normal_camera_service.normal_camera_pb2 as normal_camera_pb2
import grpc_cv_service.normal_camera_service.normal_camera_pb2_grpc as normal_camera_pb2_grpc

class NormalCameraServer(normal_camera_pb2_grpc.NormalCameraServicer):

    def __init__(self, model_path: str = "./realsense/yolo/yolo11n-seg.pt"):
        super().__init__()
        self.model_path = model_path

    def ObjectDetection(self, request, context):
        cam = cv.VideoCapture(0) # cv.VideoCapture(1, cv.CAP_DSHOW) in windows
        cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        i = 0
        model = YOLO(self.model_path)
        #model.to('cuda')
        while True:
            if found:
                break
            
            ret, cam_frame = cam.read()
            if not ret:
                break

            cam_results = model.track(cam_frame, persist=True)
            if cam_results[0].boxes.id is not None and cam_results[0].masks is not None:
                found = True
                
            i += 1
            if i > 10:
                break
        
        cam.release()
        cv.destroyAllWindows()
        return normal_camera_pb2.NormalResponse(sucess=found)

def serve():
    port = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    normal_camera_pb2_grpc.add_DepthCameraServicer_to_server(NormalCameraServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("Server started, listening on port " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
    