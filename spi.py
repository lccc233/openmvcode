from pyb import SPI,Pin
import sensor,pyb,time

spi = SPI(2, SPI.MASTER, baudrate=328125,polarity=0,phase=0,firstbit=SPI.MSB,bits=8,ti=False,crc=None)
cs  = Pin("P3", Pin.OUT_OD)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

while True:
    data1=bytearray(b'rfa')
    img = sensor.snapshot()
    cs.high()
    spi.send(data1,timeout=50)
    cs.low()

    time.sleep_ms(100)
    data=bytearray(3)
    spi.recv(data,timeout=50)
    print(data)
    time.sleep_ms(100)
