import cv2 as cv
import numpy as np

# constants
SIZE = (400, 300)

RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])

TRAP = np.float32([[0, 299],
                   [399, 299],
                   [320, 200],
                   [80, 200]])
TRAPINT = np.array(TRAP, dtype=np.int32)

# import img
img = cv.imread('s.png')
img = cv.resize(img, SIZE)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('gray', gray)

binary = cv.inRange(gray, 200, 255)
cv.imshow('bin', binary)

# tr = binary.copy()
# cv.polylines(tr, [TRAPINT], True, 255)
# cv.imshow('trap', tr)

M = cv.getPerspectiveTransform(TRAP, RECT)
perspective = cv.warpPerspective(binary, M, SIZE, flags=cv.INTER_LINEAR)
cv.imshow('perspective', perspective)

hist = np.sum(perspective[perspective.shape[0]//2:, :], axis=0)
mid = hist.shape[0]//2
left = np.argmax(hist[:mid])
right = np.argmax(hist[mid:]) + mid

cv.line(perspective, (left, 0), (left, 300), 50, 2)
cv.line(perspective, (right, 0), (right, 300), 50, 2)
cv.line(perspective, ((left + right) // 2, 0), ((left + right) // 2, 300), 110, 3)

cv.imshow('lines', perspective)
print((left + right) // 2 - 200)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
