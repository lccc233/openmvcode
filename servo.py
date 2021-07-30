from pyb import Timer
import sensor,pyb
tim = pyb.Timer(4)
tim.init(freq=2000)
p = pyb.LED(1)
counter_num=0
def tick(void):
    global counter_num
    counter_num=counter_num+1
    if counter_num==40:
        counter_num=0
    if counter_num<=1:
        p.on()
        print(1)
    else:
        p.off()
        print(0)
tim.callback(tick)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
while True:
    sensor.snapshot()
