import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from depthcamera import get_pipe, get_streams

def create_mask(results, annotator):
    if results[0].boxes.id is not None and results[0].masks is not None:
        masks = results[0].masks.xy
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for mask, track_id in zip(masks, track_ids):
            color = colors(int(track_id), True)
            txt_color = annotator.get_txt_color(color)
            annotator.seg_bbox(mask=mask, mask_color=color, label=str(track_id), txt_color=txt_color)

def main() -> None:
    cam = cv.VideoCapture(0) # cv.VideoCapture(1, cv.CAP_DSHOW) in windows
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)    
    
    pipe, align = get_pipe()
    model = YOLO('realsense/yolo/yolo11x-seg.pt')
    model.to('cuda')
    while True:
        
        """ret, cam_frame = cam.read()
        if not ret:
            break"""

        color_image, depth_image = get_streams(camera_pipe=pipe, aligned=align)
        depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)
        
        color_annotator = Annotator(color_image, line_width=2)
        depth_annotator = Annotator(depth_map, line_width=2)
        #cam_annotator = Annotator(cam_frame, line_width=2)
        
        realsense_results = model.track(color_image, persist=True)
        #cam_results = model.track(cam_frame, persist=True)

        create_mask(realsense_results, color_annotator)
        create_mask(realsense_results, depth_annotator)
        #create_mask(cam_results, cam_annotator)

        cv.imshow("depth", depth_map)
        cv.imshow("rgb", color_image)
        #cv.imshow("test", cam_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()
    pipe.stop()


main()
