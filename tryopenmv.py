import sensor#引入感光元件的模块
from pyb import UART

# 设置摄像头
sensor.reset()#初始化感光元件
sensor.set_pixformat(sensor.RGB565)#设置为彩色
sensor.set_framesize(sensor.QVGA)#设置图像的大小
sensor.skip_frames(10)#跳过n张照片，在更改设置后，跳过一些帧，等待感光元件变稳定。
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

uart = UART(3, 115200)

tag = (9, 41, 3, 63, 3, 31)

uart.write("Start work\n")
print(2)
# 一直拍照
while(True):
    if uart.any():
        order = uart.readline().decode()
        print(order,type(order))
    img = sensor.snapshot()#拍摄一张照片，img为一个image对象
    tag_blobs = img.find_blobs([tag],merge=True)
    for blob in tag_blobs:
        img.draw_rectangle(blob.rect(), color=(0,255,0))

