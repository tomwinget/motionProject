#!/usr/bin/env python

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from mpu6050 import mpu6050

f = open('data', 'r+')

sensor = mpu6050(0x68)

sleep_time = 0.001

RST = None

avg_x = 0
avg_y = 0
avg_z = 0

n = 10

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -1
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

draw.text((x,top), "Averaging sensor data...", font=font, fill=255)
disp.image(image)
disp.display()

for j in range(n):
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    accel_data = sensor.get_accel_data(True)

    avg_x+=accel_data['x']
    avg_y+=accel_data['y']
    avg_z+=accel_data['z']

    draw.text((x,top), "Accels : "+str(j), font=font, fill=255)
    draw.text((x, top+16), "Avg X: "+str(avg_x/(j+1))[:6], font=font, fill=255)
    draw.text((x, top+24), "Avg Y: "+str(avg_y/(j+1))[:6], font=font, fill=255)
    draw.text((x, top+32), "Avg Z: "+str(avg_z/(j+1))[:6], font=font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(sleep_time)

avg_x = avg_x/n
avg_y = avg_y/n
avg_z = avg_z/n

draw.rectangle((0,0,width,height), outline=0, fill=0)

disp.clear()

draw.text((x,top), "Found avg off: ", font=font, fill=255)
draw.text((x, top+16), "Avg X: "+str(avg_x)[:6], font=font, fill=255)
draw.text((x, top+24), "Avg Y: "+str(avg_y)[:6], font=font, fill=255)
draw.text((x, top+32), "Avg Z: "+str(avg_z)[:6], font=font, fill=255)

disp.image(image)
disp.display()

time.sleep(2)

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    accel_data = sensor.get_accel_data(True)
    current_time = time.clock()

    f.write(str(current_time)+','+str(accel_data['x']-avg_x)+','+str(accel_data['y']-avg_y)+','+str(accel_data['z']-avg_z)+'\n')
    
    draw.text((x,top), "Current Data: ", font=font, fill=255)
    draw.text((x,top+8), "Accel x: "+str(accel_data['x']-avg_x)[:8], font=font, fill=255)
    draw.text((x,top+16), "Accel y: "+str(accel_data['y']-avg_y)[:8], font=font, fill=255)
    draw.text((x,top+24), "Accel z: "+str(accel_data['z']-avg_z)[:8], font=font, fill=255)

    disp.image(image)
    disp.display()

    time.sleep(sleep_time)
