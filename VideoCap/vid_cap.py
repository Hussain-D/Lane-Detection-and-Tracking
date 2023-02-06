import numpy as np
import cv2

cap = cv2.VideoCapture("VideoCap/lane.mp4")
while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('output',frame)
    if(cv2.waitKey(20) & 0xFF == ord('q')):
        break
    
cap.release()
cv2.destroyAllWindows()