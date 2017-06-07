#!/usr/bin/env python

from mpu6050 import mpu6050

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

sensor = mpu6050(0x68)
f = open('data', 'r+')

avg_x = 0
avg_y = 0
avg_z = 0

n = 1000

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

draw.text((x,top), "Averaging sensor...", font=font, fill=255)
disp.image(image)
disp.display()

start = time.clock()
for x in range(n):
    accel_data = sensor.get_accel_data(True)
    avg_x = avg_x+accel_data['x']
    avg_y = avg_y+accel_data['y']
    avg_z = avg_z+accel_data['z']
end = time.clock()

avg_x = avg_x/n
avg_y = avg_y/n
avg_z = avg_z/n

draw.text((x,top), "Beginning data collection", font=font, fill=255)
disp.image(image)
disp.display()
sleep(2)

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    accel_data = sensor.get_accel_data(True)
    curTime = time.clock()
    f.write(str(accel_data['x']-avg_x)+','+str(accel_data['y']-avg_y)+','+str(accel_data['z']-avg_z)+','+str(curTime)+'\n')

    draw.text((x,top), "Current data", font=font, fill=255)
    draw.text((x, top+16), "Accel Z: "+str(accel_data['z']-avg_z), font=font, fill=255)
    disp.image(image)
    disp.display()

    time.sleep(.1)
