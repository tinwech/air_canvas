import cv2 as cv
import numpy as np

palette = cv.imread('gradient_palette.png')
width = int(palette.shape[1])
height = int(palette.shape[0])
resized_palette = cv.resize(palette, (640, 100), interpolation=cv.INTER_AREA)

def normal_palette(img, imgWidth):
    cv.rectangle(img, (0,0), (imgWidth, 100), (255,0,0), thickness=-1)
    cv.rectangle(img, (int(imgWidth * 1 / 3),0), (int(imgWidth * 2 / 3), 100), (0,255,0), thickness=-1)
    cv.rectangle(img, (int(imgWidth * 2 / 3),0), (imgWidth, 100), (0,0,255), thickness=-1)

def gradient_palette(img):
    img[0:100, 0:640] = resized_palette[0:100, 0:640]
