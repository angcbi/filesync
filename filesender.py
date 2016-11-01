#!/usr/bin/env python
# encoding: utf-8

import os
import pickle
import hashlib
import socket


def createmd5(path):
      templist = []
      config = os.path.join(path, 'filesender.ini')
      try:
            if os.path.exists(config):
                  with open(config, 'rb') as confighandler:
                        templist = pickle.load(confighandler)
            for file in os.listdir(path):
                  file = os.path.join(path, file)
                  if os.path.isfile(file):
                        tempdict = {}
                        t = hashlib.md5()
                        with open(file, 'rb') as f:
                              for data in f:
                                    t.update(data)
                        if templist:
                              if file in map(lambda x:x['filename'], templist):
                                    for i in range(len(templist)):
                                          if file == templist[i]['filename'] and t.hexdigest() != templist[i]['filename']:
                                                templist[i]['md5'] = t.hexdigest()
                                                templist[i]['flag'] = 'modify'
                              else:
                                    tempdict['filename'] = file
                                    tempdict['flag'] = 'new'
                                    tempdict['md5'] = t.hexdigest()
                                    templist.append(tempdict)
                        else:
                              tempdict['filename'] = file
                              tempdict['flag'] = 'new'
                              tempdict['md5'] = t.hexdigest()
                              templist.append(tempdict)
            with open(config, 'wb') as confighandler:
                  pickle.dump(templist, confighandler)
            return map(lambda x: x['filename'], filter(lambda x: x['flag'] in ('new', 'modify'), templist))
      except Exception, e:
            print e


def sock(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return s
    except Exception, e:
        print e

def sendFile(sock, filelist):
    for file in filelist:
        sock.send('file ' + file)
        with open(file, 'rb') as f:
            for data in f:
                sock.send(data)
        print '%s has been sended' % file


if __name__ == '__main__':
      path = '/home/caicai/Dev/Dev/my_blog'
      if os.path.exists(path):
            s = sock('', 9999)
            filelist = createmd5(path)
            sendFile(s, filelist)
      else:
            print '%s is not exists' % path


