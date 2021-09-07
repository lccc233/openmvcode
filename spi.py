from pyb import SPI,Pin
import sensor,pyb,time
spi = SPI(2, SPI.MASTER, baudrate=381005,polarity=0,phase=0,firstbit=SPI.MSB,bits=8,ti=False,crc=None)
cs  = Pin("P3", Pin.OUT_OD)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
data=bytearray(3)
cs.high()
a=1
b=6
c=1
while (True):
    a=a+1
    b=b+1
    if(a>=255): a=0
    if(b>=255): b=0
    data1=bytearray([a,b,c])
    img = sensor.snapshot()

    cs.low()
    data=spi.send_recv(data1,timeout=50)
    print(data)
    cs.high()

    time.sleep_ms(1000)
