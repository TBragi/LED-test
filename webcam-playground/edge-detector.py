import cv2
import numpy as np
import imutils

cam = cv2.VideoCapture(0)
ret, image = cam.read()

class EdgeDetector:
    def __init__(self, image) -> None:
        self.image = image
        self.dimensions = image.shape
        self.rows, self.columns = self.dimensions[0:2]
        self.channels = self.dimensions[2] if self.dimensions[2] else 1

    def displayImage(self, showImage = None, channels = None ) -> None:
        showImage = self.image if showImage is None else showImage
        if channels:
            canvas = np.zeros(shape=showImage.shape, dtype=np.uint8)
            channels = channels if isinstance(channels,list) else [channels]
            for channel in channels:
                canvas[:,:,channel] = showImage[:,:,channel]
        else:
            canvas = showImage
        while True:
            cv2.imshow('Display Image',canvas)
            k = cv2.waitKey(0)
            if k != -1:
                break
        cv2.destroyAllWindows()

edge = EdgeDetector(image) 

print(edge.__dict__)
edge.displayImage(image[:,:,:], [0,2])
cam.release()
cv2.destroyAllWindows()
