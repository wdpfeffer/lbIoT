import machine
import utime
import lbsend as lb
import SimpleClient as sc
import esp


def logger(lgstr):
    f = open('log.txt', 'a+')
    f.write(lgstr+"\n")
    f.close()


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    # logger("Deepsleep Reset Count")
    sData = lb.readLB()
    utime.sleep(1)
    sc.sendData(sData)
    utime.sleep(1)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # sleep for 10 min
    rtc.alarm(rtc.ALARM0, 1800000)
    machine.deepsleep()
    
else:
    # logger("Normal Reset")
    print('normal rest')
