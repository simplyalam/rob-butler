import numpy as np
import cv2
import create
from time import sleep
  # Display the resulting frame
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

cap = cv2.VideoCapture(1)

while(True):
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Convert BGR to HSV
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  # define range of blue color in HSV
  lower_blue = np.array([110,50,50])
  upper_blue = np.array([130,255,255])

  # Threshold the HSV image to get only blue colors
  mask = cv2.inRange(hsv, lower_blue, upper_blue)

  # Bitwise-AND mask and original image
  res = cv2.bitwise_and(frame,frame, mask= mask)



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
  help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
  help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
redLower = (160, 35, 6) #currently tracks green, UPDATE
redUpper = (10, 255, 255) #currently tracks green, UPDATE
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
  camera = cv2.VideoCapture(1)

# keep looping
while True:
  # grab the current frame
  (grabbed, frame) = camera.read()

  # resize the frame and convert it to the HSV
  # color space
  frame = imutils.resize(frame, width=600)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  # construct a mask for the color "red", then perform
  # a series of dilations and erosions to remove any small
  # blobs left in the mask
  mask = cv2.inRange(hsv, redLower, redUpper)
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=2)

  # find contours in the mask and initialize the current
  # (x, y) center of the ball
  cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
  center = None

  # only proceed if at least one contour was found
  if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # only proceed if the radius meets a minimum size
    if radius > 10:
      # draw the circle and centroid on the frame,
      # then update the list of tracked points
      cv2.circle(frame, (int(x), int(y)), int(radius),
        (0, 255, 255), 2)
      cv2.circle(frame, center, 5, (0, 0, 255), -1)

  cv2.imshow('hsv',hsv)
  cv2.imshow('frame2',frame)
  cv2.imshow('mask',mask)
  cv2.imshow('res',res)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()