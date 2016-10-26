#!/usr/bin/env python
# encoding: utf-8

import os
import pickle
import hashlib


def createmd5(path):
    templist = []
    config = os.path.join(path, 'filesender.ini')
    if os.path.exists(config):
        try:
            confighandler = open(config, 'rb')
            templist = pickle.load(confighandler)
        finally:
            confighandler.close()

    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isfile(file):
            tempdict = {}
            t = hashlib.md5()
            with open(file, 'rb') as f:
                for data in f:
                    t.update(data)
            for item in templist:
                if file not in item:
                    tempdict['flag'] = 'n'
                elif item[file] != t.hexdigest():
                    tempdict['flag'] = 'c'
                else:
                    pass
            tempdict[file] = t.hexdigest()
            templist.append(tempdict)
    try:
        confighandler = open(config, 'wb')
        pickle.dump(templist, confighandler)
    finally:
        confighandler.close()
    return templist


if __name__ == '__main__':
    # path = raw_input('Please enter a path:\n')
    path = '/home/caicai/Dev/Dev/my_blog'
    if os.path.exists(path):
        print createmd5(path)
    else:
        print '%s is not exists' % path


