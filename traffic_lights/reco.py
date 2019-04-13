import cv2

# def find(img):
#     img = cv2.resize(img, (100, 200))
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     black = cv2.inRange(gray, 0, 0)
#
#     gr = 100
#
#     bl = cv2.inRange(gray, 0, gr)
#     cv2.imshow('findbl', bl)
#     contours = cv2.findContours(bl, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
#     if contours:
#         contours = sorted(contours, key=cv2.contourArea, reverse=True)
#
#     cv2.drawContours(black, contours, 0, (255, 255, 255), cv2.FILLED)
#
#     img = cv2.bitwise_and(img, img, mask=black)
#
#     x, y, w, h = cv2.boundingRect(contours[0])
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
#     height, width, _ = img[y:y + h, x:x + w].shape
#
#     cv2.imshow('find', img[y:y + h, x:x + w])
#
#     if width > height or width*height < 10000 or w * 1.2 > h:
#         return img
#     else:
#         return img[y:y + h, x:x + w]


def recognise(cropped):
    img = cv2.resize(cropped, (100, 200))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gr = 130
    bl = cv2.inRange(gray, gr, 255)
    while cv2.countNonZero(bl) > 13000:
        gr += 5
        bl = cv2.inRange(gray, gr, 255)
    cv2.imshow('sss', bl)
    r = bl[0:70]
    y = bl[70:130]
    g = bl[130:200]

    return cv2.countNonZero(r), cv2.countNonZero(y), cv2.countNonZero(g)


def hsv_red(hsv, s1, v1, s2, v2):
    bl1 = cv2.inRange(hsv, (0, s1, v1), (95, s2, v2))
    bl2 = cv2.inRange(hsv, (165, s1, v1), (255, s2, v2))
    bl = cv2.bitwise_or(bl1, bl2)
    return bl


def recognise_hsv(cropped):
    img = cv2.resize(cropped, (100, 200))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    s = 0
    v = 240
    bl = hsv_red(hsv, s, v, 255, 255)

    # while cv2.countNonZero(bl) < 200 and v > 100:
    #     v -= 50
    #     bl = hsv_red(hsv, s, v, 255, 255)


    men = False
    # while cv2.countNonZero(bl) > 500 and not men:
    #     s += 1
    #     bl = hsv_red(hsv, s, v, 255, 255)
    #
    #     r = cv2.countNonZero(bl[0:70])
    #     y = cv2.countNonZero(bl[70:130])
    #     g = cv2.countNonZero(bl[130:200])
    #
    #     ryg = {'r': r, 'y': y, 'g': g}
    #     maxx = max(ryg, key=ryg.get)
    #     minn = min(ryg, key=ryg.get)
    #
    #     rygc = ryg.copy()
    #     rygc.pop(maxx)
    #     rygc.pop(minn)
    #
    #     men = False
    #     for e in rygc:
    #         if abs(ryg[maxx] - rygc[e]) > 1000 and cv2.countNonZero(bl) < 4000:
    #             men = True
    #             break

    cv2.imshow('hsv', bl)
    r = bl[0:70]
    y = bl[70:130]
    g = bl[130:200]

    return cv2.countNonZero(r), cv2.countNonZero(y), cv2.countNonZero(g)


def cond(r, y, g):
    ryg = {'r': r, 'y': y, 'g': g}
    maxx = max(ryg, key=ryg.get)
    minn = min(ryg, key=ryg.get)
    if ryg[maxx] - ryg[minn] < 50:
        return False

    rygc = ryg.copy()
    rygc.pop(maxx)
    for e in rygc:
        if abs(ryg[maxx] - rygc[e]) < 100:
            return False
    return True


def filereco(file):
    cap = file
    r, y, g = recognise_hsv(cap)
    # if not cond(r, y, g):
    #     r, y, g = recognise(find(cap))
    #     if not cond(r, y, g):
    #         r, y, g = recognise(cap)
    # #     if not cond(r, y, g):
    # #         r, y, g = recognise(find(cap))
    # #         if not cond(r, y, g):
    # #             r, y, g = recognise(cap)

    ryg = {0: r, 1: y, 2: g}
    maxx = max(ryg, key=ryg.get)
    return maxx
