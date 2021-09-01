import cv2
import numpy as np
import sys
import argparse

class Tracker(object):
    def __init__(self, video='NA', preview=True, hue_min=5, hue_max=6, sat_min=50, sat_max=100,
                 val_min=250, val_max=256, display_thresholds=False):
        self.video = video
        self.preview = True
        self.hue_min = hue_min
        self.hue_max = hue_max
        self.sat_min = sat_min
        self.sat_max = sat_max
        self.val_min = val_min
        self.val_max = val_max
        self.display_thresholds = display_thresholds
        self.channels = {
            'hue': None,
            'saturation': None,
            'value': None,
            'laser': None,
        }

    # def setupVideo(self):
    #
    # def run(self):

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Laser Tracker')
    # parser.add_argument('-F', '--file',
    #     default="NA",
    #     type=string,
    #     help='Video File'
    # )


    params = parser.parse_args()




    vidCapture = cv2.VideoCapture('Videos/Test.mp4')

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

            key = cv2.waitKey(5)
            if key == ord('q'):
                break
        else:
            break

    vidCapture.release()
    cv2.destroyAllWindows()
