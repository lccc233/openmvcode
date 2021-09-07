from pyb import SPI,Pin
import sensor,pyb,time
spi = SPI(2, SPI.MASTER, baudrate=3815,polarity=0,phase=0,firstbit=SPI.MSB,bits=8,ti=False,crc=None)
cs  = Pin("P3", Pin.OUT_OD)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
data=bytearray(3)

while (True):
    data1=bytearray(b'abc')
    img = sensor.snapshot()
    cs.low()
    time.sleep_us(20)
    spi.send(data1,timeout=50)
    cs.high()
    spi.recv(data,timeout=50)
    print(data)
    time.sleep_ms(10)
