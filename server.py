#!/usr/bin/env python
# encoding: utf-8


import os
import socket
from gevent.server import StreamServer

def recfile(sock, addr, filename):
    base = os.path.dirname(__file__)
    dirname = addr[0].split('.')[-1]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    try:
        while 1:
            with open(os.path.join(base, dirname, filename), 'wb') as f:
                data = sock.recv(1024)
                if not data:
                    break
                f.write(data)
        print 'recv %s done' %filename
        sock.close()

    except Exception, e:
        print e

def handle(sock, addr):
    print 'New connection from %s:%d' %addr
    data  = sock.recv(1024)
    if 'file' in data:
        filename = data.split(' ')[-1].replace('\r\n', '')
        recfile(sock, addr, filename)

s = StreamServer(('', 9999), handle)
s.serve_forever()
