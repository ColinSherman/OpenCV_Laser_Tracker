import cv2
import numpy as np
import sys
import argparse

vidCapture = cv2.VideoCapture('Videos/Test.webm')

if(vidCapture.isOpened() == False):
    print("error opening video file")
else:
    fps = vidCapture.get(5)     # 5 is the index holding the frame rate information
    print('Frames per second : ', fps,'FPS')

    frameCount = vidCapture.get(7)    # 7 is the index for fram count
    print('Frame count : ', frameCount)

while(vidCapture.isOpened()):
    ret, frame = vidCapture.read()
    if(ret == True):
        cv2.imshow('Frame!', frame)

        key = cv2.waitKey(30)
        if key == ord('q'):
            break
    else:
        break

vidCapture.release()
cv2.destroyAllWindows()
