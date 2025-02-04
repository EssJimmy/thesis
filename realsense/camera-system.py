import cv2 as cv
from ultralytics import YOLO
from depthcamera import get_pipe, get_streams

def main() -> None:
    #cam = cv.VideoCapture(1, cv.CAP_DSHOW)
    #cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    #cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    pipe, align = get_pipe()
    model = YOLO('yolo/yolo11x.pt')
    model.to('cuda')

    while True:
        #ret, cam_frame = cam.read()
        #if not ret:
        #    break

        color_image, depth_image = get_streams(camera_pipe=pipe, aligned=align)
        depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)
        
        realsense_results = model(color_image)
        for r in realsense_results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].to('cpu').detach().numpy().copy()
                c = box.cls
                bi = list(map(int, b))
                cv.rectangle(depth_map, (bi[0], bi[1], bi[2] ,bi[3]), (0, 0, 255), thickness=2, lineType=cv.LINE_4)
                cv.putText(depth_map, text=model.names[int(c)], org=(bi[0], bi[1]), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.7,
                            color=(0, 0, 255), thickness=2, lineType=cv.LINE_4)

        #cam_results = model(cam_frame)

        #cam_annotated_frame = cam_results[0].plot()
        rs_annotated_frame = realsense_results[0].plot()
        #cv.imshow("test", cam_annotated_frame)
        cv.imshow("rgb", rs_annotated_frame)
        cv.imshow("depth", depth_map)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    #cam.release()
    cv.destroyAllWindows()
    pipe.stop()

if __name__ == '__main__':
    main()
