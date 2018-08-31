from machine import Pin
import machine
import utime
import ubinascii
# import esp


# setup pins for reading state of litterbox
p4 = Pin(4, Pin.IN)
p5 = Pin(5, Pin.OUT)
p13 = Pin(13, Pin.OUT)
adc = machine.ADC(0)

def readLB():
    # turn on Pin 5 which is the transistor
    p5.on()
    utime.sleep(1)
    # turn on Pin 13 which is the relay
    p13.on()
    utime.sleep(1)
    # write the sensor values
    machineID = machine.unique_id()
    mID = str(ubinascii.hexlify(machineID)).replace("b'","").replace("'","")
    txt = mID + "," + str(p4.value()) + "," + str(adc.read())
    # turn off relay
    p13.off()
    utime.sleep(1)
    # turn off the transistor
    p5.off()
    utime.sleep(1)
    return txt
