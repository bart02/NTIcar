import cv2
import dlib
from reco import filereco

model_detector = dlib.simple_object_detector("tld.svm")

cam=cv2.VideoCapture(2)

while (1):
    ret,frame=cam.read()
    frame = cv2.resize(frame, (200, 150))

    boxes = model_detector(frame)
    if boxes:
        box = boxes[0]
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv2.imshow("Frame",frame[y:yb, x:xb])
        print(filereco(frame[y:yb, x:xb]))

    key = cv2.waitKey(1)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
cam.release()