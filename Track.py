import cv2
import numpy as np
import sys
import argparse
import imutils
import csv


class Tracker(object):
    def __init__(self, video='NA', csvName=None ,preview=True, hue_min=1, hue_max=342, sat_min=10, sat_max=100,
                 val_min=250, val_max=256, display_thresholds=False):
        self.video = video
        self.preview = True
        self.hue_min = hue_min
        self.hue_max = hue_max
        self.sat_min = sat_min
        self.sat_max = sat_max
        self.val_min = val_min
        self.val_max = val_max
        self.redLower = (hue_min,sat_min,val_min)
        self.redUpper = (hue_max,sat_max,val_max)
        self.display_thresholds = display_thresholds
        self.channels = {
            'hue': None,
            'saturation': None,
            'value': None,
            'laser': None,
        }
        self.capture = None
        self.videoWidth = None
        self.videoHeight = None
        self.videoFPS = 30
        self.writer = None
        self.csvFile = None
        self.frameCount = None
        self.csvName = csvName

    def setupVideo(self):
        self.capture = cv2.VideoCapture(self.video)
        if not self.capture.isOpened():
            sys.stderr.write("Faled to Open Video File. Quitting.\n")
            sys.exit(1)
        self.videoWidth = int(self.capture.get(3))
        self.videoHeight = self.capture.get(4)
        self.videoFPS = self.capture.get(5)
        self.frameCount = self.capture.get(7)

        return(self.capture)

    def setupCSV(self):
        self.csvFile = open(self.csvName, 'w')
        self.writer = csv.writer(self.csvFile)
        self.writer.writerow(['File:' , self.video])
        self.writer.writerow(['Height:' , str(self.videoHeight) , 'Width:' , str(self.videoWidth)])
        self.writer.writerow(['Frames:' , str(self.frameCount) , "FPS:" , str(self.videoFPS)])
        self.writer.writerow(['X','Y'])

    def calibrateCamera(self, frame):
        found, corners = cv2.findChessboardCorners(frame, (6,9))
        print(found, corners)

    def writeCSV(self, data):
        self.writer.writerow(data)

    def closeCSV(self):
        self.csvFile.close()

    def createWindow(self,name,x,y):
        cv2.namedWindow(name)
        cv2.moveWindow(name, x, y)

    def setupWindows(self):
        sys.stdout.write("Using OpenCV version: {0}\n".format(cv2.__version__))

        self.createWindow('LaserPointer', 0, 0)
        self.createWindow('RGB_VideoFrame', 10 + self.videoWidth, 0)

    def run(self):
        # self.setupWindows()
        self.setupVideo()
        self.setupCSV()
        count = 0
        while(self.capture.isOpened()):
            ret, frame = self.capture.read()
            if(ret == True):
                count = count + 1
                if count == 10:
                    self.calibrateCamera(frame)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # lower mask
                lower_red = np.array([0,40,100])
                upper_red = np.array([10,255,255])
                mask0 = cv2.inRange(hsv,lower_red,upper_red)

                # upper mask
                lower_red = np.array([170,40,100])
                upper_red = np.array([180,255,255])
                mask1 = cv2.inRange(hsv,lower_red,upper_red)

                mask = mask0 + mask1
                mask = cv2.dilate(mask, None, iterations=2)        #fill in gaps

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                center = None

                if len(cnts) > 0:
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.writeCSV(center)
                cv2.imshow('Mask', mask)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            else:
                break
        self.closeCSV()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Laser Tracker')
    parser.add_argument('-f', '--file',
                        default="Videos/Test2.mp4",
                        type=str,
                        help='Video File')
    parser.add_argument('-u', '--huemin',
                        default=5,
                        type=int,
                        help='Hue Minimum Threshold')
    parser.add_argument('-H', '--huemax',
                        default=6,
                        type=int,
                        help='Hue Maximum Threshold')
    parser.add_argument('-s', '--satmin',
                        default=100,
                        type=int,
                        help='Saturation Minimum Threshold')
    parser.add_argument('-S', '--satmax',
                        default=255,
                        type=int,
                        help='Saturation Maximum Threshold')
    parser.add_argument('-v', '--valmin',
                        default=200,
                        type=int,
                        help='Value Minimum Threshold')
    parser.add_argument('-V', '--valmax',
                        default=255,
                        type=int,
                        help='Value Maximum Threshold')
    parser.add_argument('-c', '--csv',
                        default="Track_Results.csv",
                        type=str,
                        help='CSV Output File Name')

    params = parser.parse_args()
    Track = Tracker(
        video = params.file,
        csvName = params.csv

    )
    Track.setupVideo()
    Track.run()
