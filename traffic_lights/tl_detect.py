import cv2
import dlib

model_detector = dlib.simple_object_detector("tld.svm")

cam=cv2.VideoCapture(0)

while (1):
    try:
        ret,frame=cam.read()
        frame = cv2.resize(frame, (200, 150))

        boxes = model_detector(frame)
        for box in boxes:
            print (box)
            (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
    except KeyboardInterrupt:
        break



cam.release()