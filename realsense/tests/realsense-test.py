from depthcamera import get_pipe, get_streams
import cv2 as cv

pipe, align = get_pipe()

while True:
    color_image, depth_image = get_streams(camera_pipe=pipe, aligned=align)
    
    depth_map = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.5), cv.COLORMAP_JET)

    point_x, point_y = 250, 100
    distance_mm = depth_image[point_y, point_x]

    cv.circle(color_image, (point_x, point_y), 8, (0, 0, 255), -1)
    cv.putText(color_image, f"{distance_mm} mm", (point_x, point_y-10), 0, 1, (0, 0, 255), 2)

    cv.imshow('rgb', color_image)
    cv.imshow('depth', depth_map)

    if cv.waitKey(1) == ord('q'):
        break

pipe.stop()