import lbsend as lb
import machine

html = """<!DOCTYPE html>
<html>
    <head> <title>Basement Litterbox</title>
    </head>    
    <body>
     <h1>Status</h1>
      <table border="1">
            <tr><th>ID</th><th>Status</th><th>Level</th></tr>
            %s
      </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    lbdata = lb.readLB()
    lbdata = lbdata.split(',')
    # lblevel = round((int(lbdata[2])-340)/(660-340)*100,0)
    drow='<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (lbdata[0], str(lbdata[1]), str(lbdata[2]))
    response = html % drow
    # response = html % (drow, str(lblevel), str(lblevel)+"%")
    cl.send(response)
    cl.close()

#if we get here, should reset
machine.reset()