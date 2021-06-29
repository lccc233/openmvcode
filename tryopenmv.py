import sensor
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

uart = UART(3, 115200)
tag = (34, 84, -37, 7, 25, 111)

while(True):
    if uart.any():
        order = uart.readline().decode()
        print(order,type(order))
    img = sensor.snapshot()
    tag_blobs = img.find_blobs([tag],merge=True)
    for blob in tag_blobs:
        img.draw_rectangle(blob.rect(), color=(0,255,0))

