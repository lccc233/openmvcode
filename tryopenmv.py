import sensor
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

uart = UART(1, 115200)
tag = (34, 84, -37, 7, 25, 111)

while(True):
    if(uart.any()):
        mode_read=uart.readline()
        print(mode_read[0])
    #uart.write('123')
    img = sensor.snapshot()
    tag_blobs = img.find_blobs([tag],merge=True)
    for blob in tag_blobs:
        img.draw_rectangle(blob.rect(), color=(0,255,0))
    data=bytearray([0x0f,0xa0,0x0c])
    uart.write(data)

