# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import webrepl
import network
import utime

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)
ap_if.active(False)
sta_if.ifconfig(('192.168.1.210','255.255.255.0','192.168.1.1','8.8.8.8'))
sta_if.connect('1-FBIsurveillance', 'tInKtHEGoAt06')
loopCount = 0
while loopCount < 10:
    print(loopCount)
    if sta_if.isconnected():
        print("connected", sta_if.ifconfig())
        break
    loopCount += 1
    utime.sleep(1)

gc.collect()

# attemp to loging

if sta_if.isconnected():
    webrepl.start()
    utime.sleep(1)
    import SimHTTPSer
else:
    # machine.reset()
    print("not connected")
    sta_if.active(False)
    ap_if.active(True)
    webrepl.start()