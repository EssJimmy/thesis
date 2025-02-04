import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from depthcamera import get_depth_stream_model

def __create_mask(results, annotator) -> None:
    if results[0].boxes.id is not None and results[0].masks is not None:
        masks = results[0].masks.xy
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for mask, track_id in zip(masks, track_ids):
            color = colors(int(track_id), True)
            txt_color = annotator.get_txt_color(color)
            annotator.seg_bbox(mask=mask, mask_color=color, label=str(track_id), txt_color=txt_color)


def get_cam_stream_model(model_name: str) -> None:
    cam = cv.VideoCapture(0) # cv.VideoCapture(1, cv.CAP_DSHOW) in windows
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    model = YOLO(model_name)
    model.to('cuda')
    while True:
        ret, cam_frame = cam.read()
        if not ret:
            break

        cam_annotator = Annotator(cam_frame, line_width=2)
        cam_results = model.track(cam_frame, stream=True, persist=True)
        __create_mask(cam_results, cam_annotator)
        cv.imshow("cam", cam_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()


def main() -> None:
    get_depth_stream_model()
    get_cam_stream_model()


if __name__ == '__main__':
    main()
