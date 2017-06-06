#!/usr/bin/env python
"""Released under the MIT License
Copyright 2015, 2016 MrTijn/Tijndagamer
"""

from mpu6050 import mpu6050
from time import sleep
import time

sensor = mpu6050(0x68)
f = open('data', 'r+')

avg_x= 0
avg_y= 0
avg_z= 0

n = 1000

sleep(2)

print("Averaging!")

start = time.clock()
for x in range(n):
    accel_data = sensor.get_accel_data(True)
    avg_x = avg_x+accel_data['x']
    avg_y = avg_y+accel_data['y']
    avg_z = avg_z+accel_data['z']
end = time.clock()

avg_x= avg_x/n
avg_y= avg_y/n
avg_z= avg_z/n

print("Average x: "+str(avg_x))
print("Average y: "+str(avg_y))
print("Average z: "+str(avg_z))

print("Time taken = "+str((end-start)/n))
sleep(5)

print("Collecting!")

while True:
    accel_data = sensor.get_accel_data(True)
    temp = sensor.get_temp()

    f.write(str(accel_data['x']-avg_x)+','+str(accel_data['y']-avg_y)+','+str(accel_data['z']-avg_z)+','+str(temp)+'\n')

    sleep(0.1)
