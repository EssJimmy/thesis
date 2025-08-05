import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import os
import sys
import grpc
import logging
from ultralytics import YOLO
from concurrent import futures
from datetime import datetime

DIR = os.path.dirname(__file__)
GRPC_DIR = os.path.abspath(os.path.join(DIR, "../grpc_cv_service"))
sys.path.append(GRPC_DIR)

import grpc_cv_service.depth_camera_service.depth_camera_pb2 as depth_camera_pb2
import grpc_cv_service.depth_camera_service.depth_camera_pb2_grpc as depth_camera_pb2_grpc

class RealsenseCameraServer(depth_camera_pb2_grpc.DepthCameraServicer):
    
    def __init__(self, model_name: str = "./realsense/yolo/yolo11n-seg.pt"):
        super().__init__()
        self.model_name = model_name

    def __get_pipe(self) -> tuple:
        pipe = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        align_to = rs.stream.color
        align = rs.align(align_to)

        pipe.start(config)

        return pipe, align

    def __get_streams(self, camera_pipe: object, aligned) -> tuple:
        frame = camera_pipe.wait_for_frames()
        aligned_frames = aligned.process(frame)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return color_image, depth_image
    
    def ObjectDetection(self, request, context):
        pipe, align = self.__get_pipe()
        model = YOLO(self.model_name)
        found = False
        #model.to('cuda')

        while True:
            color_image, depth_image = self.__get_streams(pipe, align)

            realsense_results = model.track(color_image, persist=True)
            i = 0
            if realsense_results[0].boxes.id is not None and realsense_results[0].masks is not None:
                while i > len(realsense_results) and not found:
                    masks = realsense_results[i].masks.xy
                    track_ids = realsense_results[i].boxes.id.int().cpu().tolist()
                    aggregate = zip(masks, track_ids)
                    x, y = map(int, np.ndarray.mean(list(aggregate)[i][0], axis=0))
                    distance_mm = depth_image[y, x]

                    if distance_mm < 850:
                        found = True
                    else:
                        i += 1

            if found:
                pipe.stop()
                return depth_camera_pb2.ObjectDetectionResponse(success=True)
            else:
                pipe.stop()
                return depth_camera_pb2.ObjectDetectionResponse(success=False)

    def DepthImage(self, request, context):
        pipe, align = self.__get_pipe()
        model = YOLO(self.model_name)
        #model.to('cuda')

        while True:
            color_image, depth_image = self.__get_streams(pipe, align)
            depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)

            realsense_results = model.track(color_image, persist=True)
            i = 0
            if realsense_results[0].boxes.id is not None and realsense_results[0].masks is not None:
                if i > len(realsense_results):
                    break
                
                masks = realsense_results[i].masks.xy
                track_ids = realsense_results[i].boxes.id.int().cpu().tolist()
                aggregate = zip(masks, track_ids)
                x, y = map(int, np.ndarray.mean(list(aggregate)[i][0], axis=0))
                distance_mm = depth_image[y, x]

                if distance_mm < 850:
                    pipe.stop()
                    return depth_camera_pb2.DepthResponse(depth_values=distance_mm,
                                                          timestamp=datetime.now().isoformat(sep=' ', timespec='microseconds')[:-8],
                                                          x_coord=x, y_coord=y)
                else:
                    i += 1
                

            cv.imshow("rgb", color_image)
            cv.imshow("depth", depth_map)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
        pipe.stop()


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    depth_camera_pb2_grpc.add_DepthCameraServicer_to_server(RealsenseCameraServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("Server started, listening on port " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
