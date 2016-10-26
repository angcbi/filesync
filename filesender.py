#!/usr/bin/env python
# encoding: utf-8

import os
import pickle
import hashlib


def createmd5(path):
      templist = []
      config = os.path.join(path, 'filesender.ini')
      try:
            confighandler = open(config, 'wb+')
            templist = pickle.load(confighandler)
            for file in os.listdir(path):
                  file = os.path.join(path, file)
                  if os.path.isfile(file):
                        tempdict = {}
                        t = hashlib.md5()
                        with open(file, 'rb') as f:
                              for data in f:
                                    t.update(data)
                        tempdict['filename'] = file
                        tempdict['md5'] = t.hexdigest()
                        if templist:
                              for i in range(len(templist)):
                                    item = templist[i]
                                    if file not in item:
                                          tempdict['flag'] = 'new'
                                    elif tempdict['md5'] != t.hexdigest():
                                          tempdict['flag'] = 'modify'
                                          tempdict['md5'] = t.hexdigest()
                                    else:
                                          pass
                              templist[i] = tempdict
                        else:
                              tempdict['flag'] = 'new'
                              templist.append(tempdict)

            pickle.dump(templist, confighandler)
            return templist
      except Exception, e:
            print e
      finally:
            confighandler.close()


if __name__ == '__main__':
      # path = raw_input('Please enter a path:\n')
      path = '/home/caicai/Dev/Dev/my_blog'
      if os.path.exists(path):
            print createmd5(path)
      else:
            print '%s is not exists' % path


