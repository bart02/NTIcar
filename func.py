import cv2 as cv
import numpy as np
import time
from servo import *

def binarize(img, d=0):
    hls = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    binaryh = cv.inRange(hls, (0, 0, 60), (255, 255, 255))

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    binaryg = cv.inRange(gray, 200, 255)

    binary = cv.bitwise_and(binaryg, binaryh)

    if d:
        cv.imshow('hls', hls)
        cv.imshow('gray', gray)
        cv.imshow('bin', binary)
    return binary


def trans_perspective(binary, trap, rect, size, d=0):
    M = cv.getPerspectiveTransform(trap, rect)
    perspective = cv.warpPerspective(binary, M, size, flags=cv.INTER_LINEAR)
    if d:
        cv.imshow('perspective', perspective)
    return perspective


timeout_detect_stop = 0
def detect_stop(perspective):
    global timeout_detect_stop
    if int(time.time()) > timeout_detect_stop + 10:
        stoplin = 0
        for i in range(50):
            stoplin += int(np.sum(perspective[i, :], axis=0) // 255)

        if stoplin > 7000:
            timeout_detect_stop = int(time.time())
            return True
        else:
            return False
    else:
        return False


def find_left_right(perspective, d=0):
    hist = np.sum(perspective[perspective.shape[0] // 2:, :], axis=0)
    mid = hist.shape[0] // 2
    left = np.argmax(hist[:mid])
    right = np.argmax(hist[mid:]) + mid
    if left <= 10 and right - mid <= 10:
        right = 399

    if d:
        cv.line(perspective, (left, 0), (left, 300), 50, 2)
        cv.line(perspective, (right, 0), (right, 300), 50, 2)
        cv.line(perspective, ((left + right) // 2, 0), ((left + right) // 2, 300), 110, 3)

        cv.imshow('lines', perspective)

    return left, right
