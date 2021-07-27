import sensor, image, time, math
from pyb import UART


clock = time.clock()
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

bnowx=0
bnearx=80
bluethresholds=[(0, 100, -14, 40, -86, -26)]
jimu_flag=2
blob_w=0
while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(bluethresholds, pixels_threshold=10, area_threshold=200, merge=True):
        roi=(blob.x(),blob.y(),blob.w(),blob.h())
        img.draw_rectangle(roi, color = (255, 255, 255))
        bnowx=(blob.x()+blob.w()/2)/4
        if bnowx<bnearx:
            bnearx=bnowx
            blob_w=blob.w()
    if abs(bnearx-35)<1.75:
        img.binary(bluethresholds)
        img.dilate(2)
        for c in img.find_circles(threshold = 5000, x_margin = 15, y_margin = 15, r_margin = 10,r_min = 20, r_max = 100, r_step = 2):
            if c:
                if abs(c.x()/4-35)<5 and abs(blob_w-2*c.r())<5:
                    #print(c.x()/4)
                    jimu_flag=1
                    img.draw_circle(c.x(), c.y(), c.r(), color = (255,0,0))
    circledata= bytearray([0xb3,0xb3,int(jimu_flag),int(bnearx),int(2),0x5b,0x0d,0x0a])
    print(jimu_flag)
    uart.write(circledata)
    print(bnearx)
    bnearx=80
    blob_w=0
    jimu_flag=2
