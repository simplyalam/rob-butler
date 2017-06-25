import create
from time import sleep

robot = create.Create("/dev/ttyUSB0")
robot.toSafeMode()



robot.go(9001)
sleep(10)
robot.stop()