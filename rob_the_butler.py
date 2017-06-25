import numpy as np
import cv2
import create
from time import sleep
from collections import deque
import argparse
import imutils

cap = cv2.VideoCapture(1)

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
redLower = (25,50,50) #currently tracks green, UPDATE
redUpper = (60,255,255) #currently tracks green, UPDATE
counter = 0
# keep looping
robot = create.Create("/dev/ttyUSB0")
robot.toSafeMode()

# Robutler movement function
##################################################################
def movement(degree_turn):

  y = int(degree_turn)

  robot.turn(y,360)
  if radius < 100:
    robot.move(2,9001)
  else:
    robot.stop()

# Color detection and camera setup
##################################################################
while True:
  # grab the current frame
  (grabbed, frame) = cap.read()

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
    if radius > 1:
      # draw the circle and centroid on the frame,
      # then update the list of tracked points
      cv2.circle(frame, (int(x), int(y)), int(radius),
        (0, 255, 255), 2)
      cv2.circle(frame, center, 5, (0, 0, 255), -1)

  cv2.imshow('hsv',hsv)
  cv2.imshow('mask',mask)
  cv2.imshow('frame2',frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
##################################################################

  while counter > 25:
    try:
      center_screen = 300
    # Number of degrees that Rob should turn
    ########################################
      c_diff = center_screen - center[0]
      degree_turn = (72/600) * c_diff
    ########################################
      counter = 0
      movement(degree_turn)
    except:
      print("Nothing here mate!")
      robot.playSong([(60,8),(64,8),(67,8),(72,8)])
      counter = 0
  counter += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
