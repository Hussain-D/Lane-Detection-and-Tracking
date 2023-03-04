import cv2
import numpy as np

def canny(image):
    grey_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gaus_img = cv2.GaussianBlur(grey_img,(5,5),0)
    cann_img = cv2.Canny(gaus_img,)
    
img = cv2.imread("sample lane image.jpg")




cv2.imshow('result',grey_img)
cv2.waitKey(0)