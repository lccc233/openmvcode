import sensor, image, time, math
from pyb import UART
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)


nearx=80
nowx=0
color=0
blob_w=0
#黄球：color=1    蓝球：color=2     红球：color=3
yellowthresholds = [(0, 100, -28, 23, 36, 127)]
bluethresholds=[(0, 100, -14, 40, -86, -26)]
redthresholds=[(0, 100, 14, 91, -6, 82)]
#积木：jimu_flag=2   球：jimu_flag=1
jimu_flag=2
while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(yellowthresholds, pixels_threshold=10, area_threshold=1000, merge=True):
        roi=(blob.x(),blob.y(),blob.w(),blob.h())
        img.draw_rectangle((blob.x(),blob.y(),blob.w(),blob.h()), color = (255,255,0))
        nowx=(blob.x()+blob.w()/2)/4
        if nowx<nearx:
            nearx=nowx
            color=1
    for blob in img.find_blobs(redthresholds, pixels_threshold=10,area_threshold=1000, merge=True):
        roi=(blob.x(),blob.y(),blob.w(),blob.h())
        img.draw_rectangle(roi, color = (255, 0, 0))
        nowx=(blob.x()+blob.w()/2)/4
        if nowx<nearx:
            nearx=nowx
            blob_w=blob.w()
            color=3
    if abs(nearx-35)<1.75:
        img.binary(redthresholds)
        img.dilate(2)
        for c in img.find_circles(threshold = 5000, x_margin = 15, y_margin = 15, r_margin = 10,r_min = 20, r_max = 100, r_step = 2):
            if c:
                if abs(c.x()/4-35)<5 and abs(blob_w-2*c.r())<5:
                    #print(c.x()/4)
                    jimu_flag=1
                    img.draw_circle(c.x(), c.y(), c.r(), color = (255,0,0))
    
                 
##################################OPENMV发数据#############################################
    data= bytearray([0xb3,0xb3,int(jimu_flag),int(nearx),int(color),0x5b,0x0d,0x0a])
    uart.write(data)
    print(jimu_flag)
    print(nearx)
    print(color)
    print("\n")
    color=0
    nearx=80
    blob_w=0
    jimu_flag=2
##################################OPENMV发数据#############################################






