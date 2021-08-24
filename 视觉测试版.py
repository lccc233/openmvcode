import sensor,time,image,pyb
from pyb import UART,Pin,Timer

aim_threshold=(22, 100, 2, 73, -14, 43)
#blue (0,100,-128,127,-92,22)
#red  (22, 100, 2, 73, -14, 43)
yellow=()
white=()
typ=-1
x_p=-1
y_p=-1
mode=-1
aim_QRCode='R\r\n'
aim_QRcode_self='R'
x_mid=160
y_mid=120
center=-1
QRresult=False
white_visible=False

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

uart1=UART(1,115200)
uart3=UART(3,115200)

tim4 = Timer(4, freq=50) # Frequency in Hz
tim2 = Timer(2, freq=50) # Frequency in Hz

ch41 = tim4.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=0)
ch42 = tim4.channel(2, Timer.PWM, pin=Pin("P8"), pulse_width_percent=0)

ch21 = tim2.channel(1, Timer.PWM, pin=Pin("P6"), pulse_width_percent=0)

def init_1():
    #复位

def init_2():
    #复位

def init_3():
    #复位

def mode_1():
    #抬头
    #收拨片
    #放头
    #夹取
    #翻转
    #松开爪子
    #抬拨片
def mode_2():
    #拨
def mode_3();
    #抓
    #等待
    #放

while(True):
    if(uart1.any()):
        mode_read=uarrt1.readline().decode().strip()
        mode=int(mode_read)
    if(mode==1):
        init_1()
    if(mode==2):
        init_2()
    if(mode==3):
        init_3()
    x_p=-1
    y_p=-1
    center=-1
    white_visible=False
    clock.tick()#
    img = sensor.snapshot()
    aim_blobs=img.find_blobs([aim_threshold],x_stride=2,y_stride=2,
                             area_threshold=6000,pixel_threshold=100,
                             merge=True,margin=2)
    yelow_blobs=img.find_blobs([yellow],x_stride=2,y_stride=2,
                               area_threshold=6000,pixel_threshold=100,
                               merge=True,margin=2)
    white_blobs=img.find_blobs([white],x_stride=2,y_stride=2,
                               area_threshold=6000,pixel_threshold=100,
                               merge=True,margin=2)
    for blob in aim_blobs:
        if(typ==-1 or abs(blob.cx()-x_mid)+abs(blob.cy()-y_mid)<center):
            x_p=blob.cx()
            y_p=blob.cy()
            center=abs(x_p-x_mid)+abs(y_p-y_mid)
            img.binary([aim_threshold])
            img.dilate(2)
            img.draw_rectangle(blob.rect(),(0,255,255))#
            detect_area=(int((blob.x()+blob.cx())/2),
                         int((blob.y()+blob.cy())/2),
                         int(blob.w()/2),int(blob.h()/2))
            statis=img.get_statistics(roi=detect_area)
            if statis.l_mean()>60:
                typ=1
                mode_2()
            else:
                typ=2
                mode_3()
            img.draw_rectangle(detect_area,(0,255,0))#
            img.draw_cross(blob.cx(),blob.cy(),size=5, color=(0,255,0))#
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

