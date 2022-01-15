import cv2
import numpy as np
import imutils

cam = cv2.VideoCapture(0)
rotation = 0
window_name = 'yikes'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, image = cam.read()
    distorted = imutils.rotate_bound(image , rotation)
    cv2.putText(distorted, 
                str(rotation), 
                (50, 50), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
    cv2.imshow(window_name,distorted)
    rotation += 1
    k = cv2.waitKey(1)
    if k != -1:
	    break
cam.release()
cv2.destroyAllWindows()
print(ret)
print(image)
