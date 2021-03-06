import sensor
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

uart = UART(1, 115200)
mode=0

class RC:
    aim_threshold = (22, 100, 2, 73, -14, 43)
    #blue (0,100,-128,127,-92,22)
    #red  (22, 100, 2, 73, -14, 43)
    yellow=()
    white=()
    x_p=-1
    y_p=-1
    x_mid=160
    y_mid=120
    center=-1
    aim_QRcode='R'
    QRok=False
    def __init__(self):
        print('Game Begain!')
    def init(self):
        self.x_p=-1
        self.y_p=-1
        self.center=-1
    def get_blob(self):
        print('blob')
        self.init()
    def get_ball(self):
        print('ball')
        self.init()
    def get_ring(self):
        print('ring')
        self.init()
    def find_aim(self):
        aim_blobs=img.find_blobs([self.aim_threshold],x_stride=2,y_stride=2,
                             area_threshold=6000,pixel_threshold=100,
                             merge=True,margin=2)
        for blob in aim_blobs:
            if(self.center==-1 or abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)<self.center):
                dis=blob.cx()-self.x_mid
                self.x_p=blob.cx()
                self.y_p=blob.cy()
                self.center=abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)
                img.binary([self.aim_threshold])
                img.dilate(2)
                img.draw_rectangle(blob.rect(),(0,255,255))#
                detect_area=(int((blob.x()+blob.cx())/2),
                             int((blob.y()+blob.cy())/2),
                             int(blob.w()/2),int(blob.h()/2))
                statis=img.get_statistics(roi=detect_area)
                img.draw_rectangle(detect_area,(0,255,0))#
                img.draw_cross(blob.cx(),blob.cy(),size=5, color=(0,255,0))#
                if statis.l_mean()>60:
                    if(abs(dis)<10):
                        self.get_blob()
                    else:
                        print('??????')
                else:
                    if(abs(dis)<10):
                        self.get_ring()
                    else:
                        print('??????')
    def find_yellow(self):
        yellow_blobs=img.find_blobs([self.yellow],x_stride=2,y_stride=2,
                               area_threshold=6000,pixel_threshold=100,
                               merge=True,margin=2)
        for blob in yellow_blobs:
            if(self.center==-1 or abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)<self.center):
                dis=blob.cx()-self.x_mid
                self.x_p=blob.cx()
                self.y_p=blob.cy()
                self.center=abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)
                if(abs(dis)<10):
                    self.get_ball()
                else:
                    print('??????')
    def find_white(self):
         self.white_blobs=img.find_blobs([self.white],x_stride=2,y_stride=2,
                               area_threshold=6000,pixel_threshold=100,
                               merge=True,margin=2)
         for blob in white_blobs:
            if(self.center==-1 or abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)<self.center):
                if(self.QRok==False):
                    for code in img.find_qrcodes():
                        if(code[4]==self.aim_QRCode):
                            self.QRok=True
                if(self.QRok==True):
                    dis=blob.cx()-self.x_mid
                    self.x_p=blob.cx()
                    self.y_p=blob.cy()
                    self.center=abs(blob.cx()-self.x_mid)+abs(blob.cy()-self.y_mid)
                    if(abs(dis)<10):
                        self.get_blob()
                    else:
                        print('??????')
    def send_message(self):
        print('????????????')
        data=bytearray([mode,0x0f,0xad])
        uart.write(data)
rc = RC()
while True:
    if uart.any():
        mode_read=uart.readline()
        print(mode_read[0])
        mode=mode_read[0]
    img = sensor.snapshot()
    if mode==1:

    rc.send_message()
