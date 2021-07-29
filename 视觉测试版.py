import sensor, time, image
from pyb import UART

aim_threshold=()
yellow=()
white=(62, 100, -10, 127, -10, 17)
typ=-1
x_p=-1
y_p=-1
aim_QRCode='R\r\n'

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

uart1=UART(1,115200)
uart3=UART(3,115200)

while(True):
    typ=-1
    x_p=-1
    y_p=-1
    clock.tick()
    img = sensor.snapshot()
    aim_blobs=img.find_blobs([aim_threshold],x_stride=2,y_stride=2,
                             area_threshold=400,pixel_threshold=100,
                             merge=True,margin=2)
    yelow_blobs=img.find_blobs([yellow],x_stride=2,y_stride=2,
                               area_threshold=200,pixel_threshold=100,
                               merge=True,margin=2)
    white_blobs=img.find_blobs([white],x_stride=2,y_stride=2,
                               area_threshold=200,pixel_threshold=100,
                               merge=True,margin=2)
    for blob in aim_blobs:
        x_p=blob.cx()
        y_p=blob.cy()
        img.binary([aim_threshold])
        img.erode(2)
        img.dilate(3)
        img.draw_rectangle(blob.rect(),(0,255,255))
        statis=img.get_statistics(roi=(x_p-25,y_p-25,50,50))
        if statis.l_mean()>50:
            typ=1
        else:
            typ=2
    for blob in yelow_blobs:
        x_p=blob.cx()
        y_p=blob.cy()
        typ=3
        img.draw_rectangle(blob.rect(),(255,0,0))
    for blob in white_blobs:
        if(uart3.any()):
            QRCode = uart3.readline().decode()
            if(QRCode==aim_QRCode):typ=1
        x_p=blob.cx()
        y_p=blob.cy()
        img.draw_rectangle(blob.rect(),(255,255,255))
    data=bytearray([0xee,0xee,0xee,int(typ),int(x_p),int(y_p)])
    uart1.write(data)
    print(data)
    print("FPS %f"%clock.fps())
