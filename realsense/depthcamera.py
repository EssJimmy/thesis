import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

def __create_mask(annotator, masks, track_ids) -> None:
    for mask, track_id in zip(masks, track_ids):
        color = colors(int(track_id), True)
        txt_color = annotator.get_txt_color(color)
        annotator.seg_bbox(mask=mask, mask_color=color, label=str(track_id), txt_color=txt_color)


def __get_pipe() -> tuple:
    pipe = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    align_to = rs.stream.color
    align = rs.align(align_to)

    pipe.start(config)

    return pipe, align


def __get_streams(camera_pipe: object, aligned) -> tuple:
    frame = camera_pipe.wait_for_frames()
    aligned_frames = aligned.process(frame)

    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    return color_image, depth_image


def get_depth_stream_model(model_name: str) -> None:
    pipe, align = __get_pipe()
    model = YOLO(model_name)
    #model.to('cuda')

    while True:
        color_image, depth_image = __get_streams(pipe, align)
        depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)

        color_annotator = Annotator(color_image, line_width=2)
        depth_annotator = Annotator(depth_map, line_width=2)

        realsense_results = model.track(color_image, persist=True)
        i = 0
        if realsense_results[0].boxes.id is not None and realsense_results[0].masks is not None:
            if i > len(realsense_results):
                i = 0
            
            masks = realsense_results[i].masks.xy
            track_ids = realsense_results[i].boxes.id.int().cpu().tolist()
            aggregate = zip(masks, track_ids)
            x, y = map(int, np.ndarray.mean(list(aggregate)[i][0], axis=0))
            distance_mm = depth_image[y, x]
            print(distance_mm)

            if distance_mm < 850:
                cv.putText(color_image, f"{distance_mm} mm", (x, y-10), 0, 1, (0, 0, 255), 2)
                cv.circle(color_image, (x, y), 8, (0, 0, 255), -1)
            else:
                i += 1

            __create_mask(color_annotator, masks, track_ids)
            __create_mask(depth_annotator, masks, track_ids)

        cv.imshow("rgb", color_image)
        cv.imshow("depth", depth_map)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    pipe.stop()