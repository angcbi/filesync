#!/usr/bin/env python
# encoding: utf-8

import os
from gevent.server import StreamServer


def handledata(data):
      print data
      try:
            tempList = data.split('EOF')
            if not tempList:
                  print 'no EOF received'
                  return None
            print tempList
            for item in tempList:
                  if not item:
                      continue
                  dd = item.split('START')
                  try:
                        filename = dd[0]
                        filedata = ('').join(dd[1:])
                        print 'receive file ', filename
                        total = 0
                        with open(os.path.join('/home/caicai/Dev/Dev/', filename), 'wb') as f:
                              for d in filedata:
                                    total += len(d)
                                    f.write(d)
                                    # sys.stdout.write(str(total) + '\r')
                                    # sys.stdout.flush()
                        print 'receive done'
                  except Exception, e:
                        print e
      except :
            pass

def handle(sock, addr):
      print 'New connection from %s:%d' % addr
      res = ''
      while 1:
            data = sock.recv(1024)
            if not data:
                  break
            res += data
      handledata(res)


s = StreamServer(('', 8888), handle)
s.serve_forever()

