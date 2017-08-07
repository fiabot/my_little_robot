import Robot 
import time 

throttle = 100.0


print("fast turn") 
move_gen(-throttle,throttle,1) 

print("medium turn") 
move_gen(0,throttle,1) 

print("slow turn") 
move_gen(throttle/2,throttle,1) 
