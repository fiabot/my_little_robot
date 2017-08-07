import Robot 
import time 

LEFT_TRIM   = -4
RIGHT_TRIM  = 0

throttle = 100
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM) #define the robot


print("fast turn") 
robot.move_gen(-throttle,throttle,3) 

time.sleep(1)

print("medium turn") 
robot.move_gen(0,throttle,1) 
time.sleep(1)

print("slow turn") 
robot.move_gen(throttle/2,throttle,1) 
time.sleep(1)
