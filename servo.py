from pyb import Timer
import sensor,pyb,time
tim = pyb.Timer(4)
tim.init(freq=4000)
p = pyb.Pin("P0", pyb.Pin.OUT_PP)
p.low()
counter_num=0
aim_counter=1
def tick(void):
    global counter_num
    counter_num=counter_num+1
    if counter_num==80:
        counter_num=0
    if counter_num<=aim_counter:
        p.high()
        print(1)
    else:
        p.low()
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
    print(1)

