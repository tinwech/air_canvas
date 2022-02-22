import cv2 as cv
import mediapipe as mp
import time
import numpy as np
from palette import *

cap = cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0,0,255), thickness=8)
handConStyle = mpDraw.DrawingSpec(color=(0,255,0), thickness=5)
alpha = 0.4
pTime = 0
cTime = 0
iPos = (0,0)
mPos = (0,0)
brushColor = (0,0,255)
points = []


def show_fps():
    global pTime
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, f'FPS: {int(fps)}', (30, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255))

def show_pointer():
    global brushColor
    dx = iPos[0] - mPos[0]
    dy = iPos[1] - mPos[1]
    d2 = dx**2 + dy**2
    if d2 > 2000:
        cv.circle(img, iPos, 10, brushColor, thickness=-1)
        points.append((iPos, brushColor))
    else:
        midPoint = (int(iPos[0] * 0.5 + mPos[0] * 0.5), int(mPos[1] * 0.5 + mPos[1] * 0.5))
        cv.circle(canvas, iPos, 15, brushColor, thickness=2)
        if midPoint[0] >= 0 and midPoint[0] < imgWidth and midPoint[1] >= 0 and midPoint[1] < 100:
            b, g, r = palette_img[midPoint[1], midPoint[0]]
            brushColor = (int(b), int(g), int(r))
            cv.circle(img, midPoint, 8, brushColor, thickness=-1)
        
def show_hand():
    global iPos, mPos
    if result.multi_hand_landmarks:
        overlay = img.copy()
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(overlay, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
        cv.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        for i, lm in enumerate(handLms.landmark):
            xPos = int(lm.x * imgWidth)
            yPos = int(lm.y * imgHeight)
            if i == 8: #index finger
                iPos = (xPos, yPos)
            elif i == 12: #middle finger
                mPos = (xPos, yPos)

def draw():
    for pos, color in points:
        cv.circle(canvas, pos, 15, color, thickness=-1)
        
while True:
    ret, img = cap.read()
    img = cv.flip(img, 1)
    if ret:
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        canvas = np.zeros(img.shape, dtype='uint8')
        #normal_palette(img, imgWidth)
        gradient_palette(img)
        palette_img = img.copy()
        show_hand()
        show_pointer()
        show_fps()
        draw()
        cv.imshow('img', img)
        cv.imshow('canvas', canvas)

    if cv.waitKey(1) == ord('q'):
        break
