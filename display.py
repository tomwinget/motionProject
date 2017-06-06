#!/usr/bin/env python
# Script for displaying info on screen
# Author: Tom Winget

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from mpu6050 import mpu6050

import subprocess

# Create sensor
sensor = mpu6050(0x68)

# RPi pin config:
RST = None

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3c)

# Open file
f = open('data', 'r+')

# Init library
disp.begin()

# Clear Display
disp.clear()
disp.display()

# Create blank image for drawing ( mode '1' for 1-bit color)
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw black fill to clear image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw shapes and define constants for easy resize
padding = -2
top = padding
bottom = height-padding
# Move left to right to track current x position to draw shapes
x=0

# Load default font
font = ImageFont.load_default()

# Generate avg values
avg_x = 0
avg_y = 0
avg_z = 0

n = 1000

time.sleep(2)

# Display averaging message
draw.text((x, top), "Averaging sensor...", font=font, fill=255)
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

print("Collecting Data!")
while True:
    count = 0

    # Draw filled box to clear image
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for now
    #cmd = "hostname -I | cut -d\' \' -f1"
    #IP = subprocess.check_output(cmd, shell = True)
    #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    #CPU = subprocess.check_output(cmd, shell = True)
    #cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    #MemUse = subprocess.check_output(cmd, shell = True)
    #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3, $2, $5}'"
    #Disk = subprocess.check_output(cmd, shell = True)

    # Accelerometer data
    accel_data = sensor.get_accel_data(True)
    temp = sensor.get_temp()
    temp = temp*9/5
    temp = temp + 32
    temp = str(temp)[:4]
    accel_x = accel_data['x']-avg_x
    accel_y = accel_data['y']-avg_y
    accel_z = accel_data['z']-avg_z
    #current_time = time.clock()
    #f.write(str(current_time)+','+str(accel_x-avg_x)+','+str(accel_y-avg_y)+','+str(accel_z-avg_z)+','+str(temp)+'\n')

    # Write two lines of text
    #draw.text((x, top), "IP: " + str(IP), font = font, fill=255)
    #draw.text((x, top+8), str(CPU), font = font, fill=255)
    #draw.text((x, top+16), str(MemUse), font = font, fill=255)
    #draw.text((x, top+24), str(Disk), font = font, fill=255)
    #draw.text((x, top+32), "A. Temp: "+temp, font = font, fill=255)
    draw.text((x, top), "A. z: "+str(accel_z), font = font, fill=255)
    #draw.text((x, top+40), "A. x: "+str(accel_x)[:4]+" y: "+str(accel_y)[:4]+" z: "+str(accel_z)[:4], font = font, fill=255)

    disp.image(image)
    disp.display()
    time.sleep(.5)
