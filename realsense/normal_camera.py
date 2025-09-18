import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

def __create_mask(masks, track_ids, annotator) -> None:
    for mask, track_id in zip(masks, track_ids):
        color = colors(int(track_id), True)
        txt_color = annotator.get_txt_color(color)
        annotator.seg_bbox(mask=mask, mask_color=color, label=str(track_id), txt_color=txt_color)


def get_cam_stream_model(model_path: str = "./realsense/yolo/yolo11n-seg.pt") -> None:
    cam = cv.VideoCapture(0) # cv.VideoCapture(1, cv.CAP_DSHOW) in windows
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    model = YOLO(model_path)
    #model.to('cuda')
    while True:
        ret, cam_frame = cam.read()
        if not ret:
            break

        cam_annotator = Annotator(cam_frame, line_width=2)
        cam_results = model.track(cam_frame, persist=True)
        if cam_results[0].boxes.id is not None and cam_results[0].masks is not None:
            masks = cam_results[0].masks.xy
            track_ids = cam_results[0].boxes.id.int().cpu().tolist()
            __create_mask(masks, track_ids, cam_annotator)
            
            cv.imshow("cam", cam_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    get_cam_stream_model()