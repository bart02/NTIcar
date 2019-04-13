import cv2 as cv
import numpy as np
from func import *


KP = 0.2
KI = 0
KD = 0
last = 0
integral = 0

# constants
SIZE = (400, 300)

RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])

TRAP = np.float32([[0, 299],
                   [399, 299],
                   [330, 200],
                   [70, 200]])
TRAPINT = np.array(TRAP, dtype=np.int32)

cap = cv.VideoCapture(2)

while True:
    try:
        ret, frame = cap.read()
        img = cv.resize(frame, SIZE)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        binaryg = cv.inRange(gray, 0, 50)
        cv.imshow('svt', binaryg)

        # print trap
        # tr = binary.copy()
        # cv.polylines(tr, [TRAPINT], True, 255)
        # cv.imshow('trap', tr)
        #
        # perspective = trans_perspective(binary, TRAP, RECT, SIZE, 1)
        #
        # if detect_stop(perspective):
        #     print('stop_detected')
        #
        # left, right = find_left_right(perspective, 1)
        #
        # err = 0 - ((left + right) // 2 - 200)
        # if abs(right - left) < 100:
        #     err = last
        # # print(err)
        # pid = KP * err + KD * (err - last) + KI * integral
        # last = err
        # integral += err

        # control(pi, ESC, 1540, STEER, 90 + pid)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        break

cv.destroyAllWindows()
cap.release()
