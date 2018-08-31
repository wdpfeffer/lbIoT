import socket
import time
import datetime as dt
import smtplib
import signal
import sys
from servDB import DB
# import ThawDB as tb


def dateNow():
    dNow = dt.datetime.now()
    dateString = str(dNow.year) + str(dNow.month).zfill(2) \
        + str(dNow.day).zfill(2) + str(dNow.hour).zfill(2) \
        + str(dNow.minute).zfill(2) + str(dNow.second).zfill(2)
    return dateString

def SendMail(addrToSend, subj, msg):
    pw = "Iamthekey03!"
    emailaddr = "info@willowmtsci.com"
    smtpObj = smtplib.SMTP('mail.willowmtsci.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(emailaddr, pw)
    smtpObj.sendmail(emailaddr, addrToSend, 'Subject: '+subj + '\n' + msg)
    {}
    smtpObj.quit()

def sigHandler(signum, frame):
    print('Signal handler called with signal', signum)
    raise IOError('Couldnt complete communication')

def getSocket(addr):
    s = socket.socket()
    print('socket created')
    s.bind(addr)
    print('socket bound')
    time.sleep(1)
    s.listen(1)
    time.sleep(1)
    return s

addr = socket.getaddrinfo('0.0.0.0', 33733)[0][-1]
s = getSocket(addr)
print('socket listening at', dateNow())

# create a file for storing data
fname = "f"+dateNow()+".csv"

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        # prepare for 2 way comm. Fail after sec 10sec
        signal.signal(signal.SIGALRM, sigHandler)
        signal.alarm(10)
        response = "ready".encode('utf-8')
        cl.send(response)
        msg = cl.recv(100).decode('utf-8')
        if (msg[len(msg)-1] == ","):
            msg = msg[0:len(msg)-1]

        # print the msg
        print(msg)

        # cancel the alarm.
        signal.alarm(0)

        # convert data to list
        dlist = msg.split(",")
        
        # update database
        db=DB()
        db.updatesvIOT(1, dlist[1])
        db.updatesvIOT(3, dlist[2])
        db.close()

    except IOError:
        try:
            cl.close()
        except:
            print('Error in closing cl')

        print("IO error")

    except KeyboardInterrupt:
        try:
            cl.close()
        except:
            print('Error in closing cl')

        print('Keyboard exception. Most likely ctrl-c')

        exit()

    except:
        try:
            cl.close()
        except:
            print('Error in closeing cl')

        print('Unknown error', sys.exc_info()[0])