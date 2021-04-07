import cv2
import math


def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(pointsList)
        if size != 0 and size % 3 != 0:
            cv2.line(img, tuple(pointsList[round((size-1)/3)*3]), (x, y), (0, 0, 255), 2)
        cv2.circle(img, (x, y), 3, (0, 0, 255), cv2.FILLED)
        pointsList.append([x, y])



def gradient(p1, p2):
    if p1[0] == 0:
        p1[0] == 1
    elif p1[1] == 0:
        p1[1] == 1
    return (p2[1]-p1[1])/(p2[0]-p1[0]+1e-10)


def getAngle(pointsList):
    p1, p2, p3 = pointsList[-3:]
    m1 = gradient(p1, p2)
    m2 = gradient(p1, p3)
    angR = math.atan((m2-m1)/(1+m2*m1))
    angD = round(math.degrees(angR))

    cv2.putText(img, str(abs(angD)), (p1[0]-40, p1[1]-20), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)


path = "C:\\Users\\Housemaster\\Desktop\\Programming\\Python\\Work\\OpenCV\\Real Projects\\Angle detection\\test2.jpg"
img = cv2.imread(path)
pointsList = []

while True:
    if len(pointsList) % 3 == 0 and len(pointsList) != 0:
        getAngle(pointsList)
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pointsList = []
        img = cv2.imread(path)
    if cv2.waitKey(1) & 0xFF == ord('b'):
        break