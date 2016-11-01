#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import socket

def recv_all(sock, file_name, file_size):
    f = open(file_name, 'wb')
    while file_size > 0:
        if file_size <= 1024:
            data = sock.recv(1024)
            f.write(data)
            break
        elif file_size > 1024:
            data = sock.recv(1024)
            file_size -= 1024
    f.close()

try:
    s = socket.create_connection(('192.168.1.36', 8888))
    while 1:
        commands = raw_input('>>>')
        s.send(commands)
        options = commands.strip().split()
        if len(options) == 2:
            file_name = options[1]
            if options[0] == 'put':
                f = open(file_name)
                data = f.read()
                time.sleep(0.2)
                s.send(str(len(data)))
                time.sleep(0.2)
                s.send(data)
                print s.recv(1024)
            elif options[0] == 'get':
                file_size = int(s.recv(1024))
                recv_all(s, file_name, file_size)
                print s.recv(1024)
        else:
            pass
except Exception, e:
    print e
