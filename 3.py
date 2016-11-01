#!/usr/bin/env python
# encoding: utf-8

import time
from gevent.server import StreamServer


def handledata(sock, filename, file_size):
    try:
        print 'receive file %s' %filename
        with open('/tmp/' + filename, 'wb') as f:
            while  file_size > 0:
                if file_size <= 1024:
                    data = sock.recv(1024)
                    f.write(data)
                    break
                elif file_size > 1024:
                    data = sock.recv(1024)
                    f.write(data)
                    file_size -= 1024
    except Exception, e:
        print e

def handle(sock, addr):
      print 'New connection from %s:%d' % addr
      while 1:
            data = sock.recv(1024)
            print data
            options = data.strip().split(' ')
            if len(options) == 2:
                file_name = options[1]
                if options[0] == 'put':
                    file_size = sock.recv(1024)
                    print file_size
                    file_size = int(file_size)
                    handledata(sock, file_name, file_size)
                    sock.sendall('Done')
                elif options[0] == 'get':
                    f = open('/tmp/%s' % file_name)
                    data = f.read()
                    sock.send(str(len(data)))
                    time.sleep(0.2)
                    sock.sendall(data)
                    time.sleep(0.2)
                    sock.send('Done')


s = StreamServer(('', 8888), handle)
s.serve_forever()

