import pyrealsense2 as rs
import numpy as np

def get_pipe() -> tuple:
    pipe = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    align_to = rs.stream.color
    align = rs.align(align_to)

    pipe.start(config)

    return pipe, align


def get_streams(camera_pipe: object, aligned) -> tuple:
    frame = camera_pipe.wait_for_frames()
    aligned_frames = aligned.process(frame)

    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    return color_image, depth_image
