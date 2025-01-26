import cv2 as cv
import threading
from multiprocessing import Pool
from depthcamera import get_pipe, get_streams

cam = cv.VideoCapture(1, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
pipe = get_pipe()

cv.namedWindow("test")
while True:
    ret, frame = cam.read()
    if not ret:
        break

    color_image, depth_image = get_streams(camera_pipe=pipe)
    depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)
    
    cv.imshow("depth", depth_map)
    cv.imshow("test", frame)
    cv.imshow("rgb", color_image)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
pipe.stop()
