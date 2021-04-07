import cv2 as cv
import numpy as np
import math


def gradient(p1, p2):
    if p1[0] == 0:
        p1[0] == 1
    elif p1[1] == 0:
        p1[1] == 1
    return (p2[1]-p1[1])/(p2[0]-p1[0]+1e-10)


def getAngle(pointsList):
    p1, p2, p3 = (x1, y1), (x2, y2), (720, y1)
    m1 = gradient(p1, p2)
    m2 = gradient(p1, p3)
    angR = math.atan((m2-m1)/(1+m2*m1))
    angD = round(math.degrees(angR))
    return angD


def nothing(x):
    pass


cap = cv.VideoCapture(0)
font = cv.FONT_HERSHEY_COMPLEX
kernel = np.ones((5, 5), np.uint8)


cv.namedWindow('Tracking Blue')
cv.createTrackbar('LowerHue', 'Tracking Blue', 21, 180, nothing)
cv.createTrackbar('LowerSat', 'Tracking Blue', 139, 255, nothing)
cv.createTrackbar('LowerValue', 'Tracking Blue', 0, 255, nothing)
cv.createTrackbar('UpperHue', 'Tracking Blue', 124, 180, nothing)
cv.createTrackbar('UpperSat', 'Tracking Blue', 255, 255, nothing)
cv.createTrackbar('UpperValue', 'Tracking Blue', 255, 255, nothing)

cv.namedWindow('Tracking Red')
cv.createTrackbar('LowerHue', 'Tracking Red', 0, 180, nothing)
cv.createTrackbar('LowerSat', 'Tracking Red', 83, 255, nothing)
cv.createTrackbar('LowerValue', 'Tracking Red', 121, 255, nothing)
cv.createTrackbar('UpperHue', 'Tracking Red', 180, 180, nothing)
cv.createTrackbar('UpperSat', 'Tracking Red', 174, 255, nothing)
cv.createTrackbar('UpperValue', 'Tracking Red', 213, 255, nothing)


while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)

    hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    l_h = cv.getTrackbarPos('LowerHue', 'Tracking Blue')
    l_s = cv.getTrackbarPos('LowerSat', 'Tracking Blue')
    l_v = cv.getTrackbarPos('LowerValue', 'Tracking Blue')
    u_h = cv.getTrackbarPos('UpperHue', 'Tracking Blue')
    u_s = cv.getTrackbarPos('UpperSat', 'Tracking Blue')
    u_v = cv.getTrackbarPos('UpperValue', 'Tracking Blue')
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    Mask = cv.inRange(hsv_img, l_b, u_b)
    Mask = cv.erode(Mask, kernel, iterations=1)
    Mask = cv.morphologyEx(Mask, cv.MORPH_OPEN, kernel)
    Mask = cv.dilate(Mask, kernel, iterations=1)
    resB = cv.bitwise_and(frame, frame, mask=Mask)

    rl_h = cv.getTrackbarPos('LowerHue', 'Tracking Red')
    rl_s = cv.getTrackbarPos('LowerSat', 'Tracking Red')
    rl_v = cv.getTrackbarPos('LowerValue', 'Tracking Red')
    ru_h = cv.getTrackbarPos('UpperHue', 'Tracking Red')
    ru_s = cv.getTrackbarPos('UpperSat', 'Tracking Red')
    ru_v = cv.getTrackbarPos('UpperValue', 'Tracking Red')
    rl_b = np.array([rl_h, rl_s, rl_v])
    ru_b = np.array([ru_h, ru_s, ru_v])
    rMask = cv.inRange(hsv_img, rl_b, ru_b)
    rMask = cv.erode(rMask, kernel, iterations=1)
    rMask = cv.morphologyEx(rMask, cv.MORPH_OPEN, kernel)
    rMask = cv.dilate(rMask, kernel, iterations=1)
    resR = cv.bitwise_and(frame, frame, mask=rMask)

    pic = cv.bitwise_or(resB, resR)

    moments1 = cv.moments(Mask.copy())
    moments2 = cv.moments(rMask.copy())
    area1 = moments1['m00']
    area2 = moments2['m00']

    x1, y1, x2, y2 = (1, 2, 3, 4)
    coord_list = [x1, y1, x2, y2]
    for x in coord_list:
        x = 0

    if area1 > 200000:
        x1 = int(moments1['m10'] / area1)
        y1 = int(moments1['m01'] / area1)
        cv.circle(frame, (x1, y1), 5, (255, 255, 255), -1)
    if area2 > 200000:
        x2 = int(moments2['m10']/area2)
        y2 = int(moments2['m01']/area2)
        cv.circle(frame, (x2, y2), 5, (255, 255, 255), -1)

        cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv.LINE_AA)

        cv.line(frame, (x1, y1), (720, y1), (0, 255, 0), 4, cv.LINE_AA)
    if y2 == 0:
        y2 = 1
    elif x1 == 0:
        x1 = 1
    angle = getAngle(coord_list)
    if angle < 0:
        angle = angle + 180
    cv.putText(frame, str(abs(angle)), (x1 + 50, int((y2 + y1) / 2)), font, 4, (255, 255, 255))

    cv.imshow('frame', frame)
    cv.imshow('mask R', resR)
    cv.imshow('mask B', resB)
    cv.imshow('res', pic)

    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
