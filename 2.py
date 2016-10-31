#!/usr/bin/env python
# encoding: utf-8

import sys
import socket

try:
    #files = ('aa.txt', 'bb.txt', '111.jpg', 'test.bin')
    files = ('aa.txt', 'bb.txt')
    # files = ('aa.txt', )
    s = socket.create_connection(('127.0.0.1', 8888))
    for item in files:
        s.send(item + 'START')
        print 'send file ', item
        total = 0
        with open(item, 'rb') as f:
            for data in f:
                total += len(data)
                s.send(data)
                print 'send ', total
                sys.stdout.write('send '+ str(total) + '\r')
                sys.stdout.flush()
        s.send('EOF')
        print 'EOF'
    s.close()
except Exception, e:
    print e
