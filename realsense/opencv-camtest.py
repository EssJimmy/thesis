import cv2 as cv

cam = cv.VideoCapture(1, cv.CAP_DSHOW)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

cv.namedWindow("test")
while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv.imshow("test", frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()