import sensor,time,image,math,pyb
from pyb import UART

aim_threshold=(1,100,1,31,-55,-5)
yellow=()
white=(62, 100, -10, 127, -10, 17)
typ=-1
x_p=-1
y_p=-1
aim_QRCode='R\r\n'
aim_QRcode_self='R'
x_mid=160
y_mid=120
center=-1
QRresult=False
white_visible=False

red_led=pyb.LED(1)
green_led=pyb.LED(2)
blue_led=pyb.LED(3)
ir_led=pyb.LED(4)
red_led.on()
green_led.on()
blue_led.on()
ir_led.on()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
#sensor.set_auto_gain(False)
#sensor.set_auto_whitebal(False)
clock = time.clock()#

uart1=UART(1,115200)
uart3=UART(3,115200)

red_led.off()
green_led.off()
blue_led.off()
ir_led.off()

while(True):
    typ=-1
    x_p=-1
    y_p=-1
    center=-1
    white_visible=False
    clock.tick()#
    img = sensor.snapshot()
    aim_blobs=img.find_blobs([aim_threshold],x_stride=2,y_stride=2,
                             area_threshold=1000,pixel_threshold=100,
                             merge=True,margin=2)
    yelow_blobs=img.find_blobs([yellow],x_stride=2,y_stride=2,
                               area_threshold=1000,pixel_threshold=100,
                               merge=True,margin=2)
    white_blobs=img.find_blobs([white],x_stride=2,y_stride=2,
                               area_threshold=1000,pixel_threshold=100,
                               merge=True,margin=2)
    for blob in aim_blobs:
        if(typ==-1 or abs(blob.cx()-x_mid)+abs(blob.cy()-y_mid)<center):
            x_p=blob.cx()
            y_p=blob.cy()
            center=abs(x_p-x_mid)+abs(y_p-y_mid)
            img.binary([aim_threshold])
            img.dilate(2)
            img.draw_rectangle(blob.rect(),(0,255,255))#
            statis=img.get_statistics(roi=(x_p-25,y_p-25,50,50))
            if statis.l_mean()>50:
                typ=1
            else:
                typ=2
    for blob in yelow_blobs:
        if(typ==-1 or abs(blob.cx()-x_mid)+abs(blob.cy()-y_mid)<center):
            x_p=blob.cx()
            y_p=blob.cy()
            center=abs(x_p-x_mid)+abs(y_p-y_mid)
            typ=3
            img.draw_rectangle(blob.rect(),(255,0,0))#
    for blob in white_blobs:
        white_visible=True
        img.draw_rectangle(blob.rect(),(255,255,255))#
        if(typ==-1 or abs(blob.cx()-x_mid)+abs(blob.cy()-y_mid)<center):
            if QRresult:
                typ=1
                x_p=blob.cx()
                y_p=blob.cy()
                center=abs(x_p-x_mid)+abs(y_p-y_mid)
                break;
            for code in img.find_qrcodes():
                print(code[4])#
                if code[4]==aim_QRcode_self:
                    typ=1
                    x_p=blob.cx()
                    y_p=blob.cy()
                    center=abs(x_p-x_mid)+abs(y_p-y_mid)
                    QRresult=True
            if QRresult:
                break
            if(uart3.any()):
                QRCode = uart3.readline().decode()
                if(QRCode==aim_QRCode):
                    typ=1
                    x_p=blob.cx()
                    y_p=blob.cy()
                    center=abs(x_p-x_mid)+abs(y_p-y_mid)
                    QRresult=True
    if white_visible==False:
        QRresult=False
    print(QRresult)
    if(typ!=-1 and x_p!=-1 and y_p!=-1):
        x_p=int(x_p/2)
        y_p=int(y_p/2)
        print(x_p)
        print(y_p)
        data=bytearray([0xff,0xfe,typ,x_p,y_p])
        uart1.write(data)
        print(data)
    print("FPS %f"%clock.fps())#
