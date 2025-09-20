import cv2 as cv
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

cv.namedWindow("test")
model = YOLO("yolo11x-seg.pt")
model.to("cuda")
while True:
    ret, frame = cam.read()
    if not ret:
        break

    annotator = Annotator(frame, line_width=2)

    results = model.track(frame, persist=True)
    if results[0].boxes.id is not None and results[0].masks is not None:
        masks = results[0].masks.xy
        track_ids = results[0].boxes.id.int().cpu().tolist()

        for mask, track_id in zip(masks, track_ids):
            color = colors(int(track_id), True)
            txt_color = annotator.get_txt_color(color)
            annotator.seg_bbox(mask=mask, mask_color=color, label=str(track_id), txt_color=txt_color)

    cv.imshow("test", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()