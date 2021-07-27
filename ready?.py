import sensor,time
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

uart = UART(3, 115200)
clock=time.clock()

yellow=[(20,89,-23,26,40,111)]
blue=[(0,93,-26,59,-57,-5)]
red=[(8,98,9,106,-12,127)]

while(True):
    uart.write('1')
    clock.tick()
    img=sensor.snapshot()
    blobs_yellow=img.find_blobs(yellow,merge=True,area_threshold=2000)
    for blob in blobs_yellow:
        img.draw_rectangle(blob.rect(), color=(255,255,0))
    blobs_blue=img.find_blobs(blue,merge=True,area_threshold=2000)
    for blob in blobs_blue:
        img.draw_rectangle(blob.rect(), color=(0,0,255))
        img.binary(blue)
        img.erode(2)
        img.dilate(2)
        for c in img.find_circles(threshold = 5000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 50, r_max = 1000, r_step = 2):
                img.draw_circle(c.x(), c.y(), c.r(), color = (0, 0, 255))
    blobs_red=img.find_blobs(red,merge=True,area_threshold=2000)
    for blob in blobs_red:
        img.draw_rectangle(blob.rect(), color=(255,0,0))
    #print(clock.fps())
