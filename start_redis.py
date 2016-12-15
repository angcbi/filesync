#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import time
import socket
import commands
import logging
import traceback
try:
      from redis import StrictRedis
except:
      pass

NODES = [
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6379,
      'maxmemory': '2G'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6380,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6381,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6382,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6385,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6386,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6387,
      'maxmemory': '250M'
      },
      {
      'host': '192.168.1.36',
      'password': '',
      'port': 6388,
      'maxmemory': '100M'
      },
]


class MyRedis():
      def __init__(self, host, port, password, maxmemory):
            self.logger = self.__class__.createLogger()
            self.host = host
            self.port = port
            self.password = password
            self.maxmemory = maxmemory
            self.configPath = '/usr/local/cluster-test/etc'
            self.loggerError('*'*50)

      @staticmethod
      def getAddr():
            try:
                  raise KeyError('11')
                  return socket.gethostbyname_ex(socket.getfqdn())[-1]
            except:
                  res =  commands.getstatusoutput('ifconfig -a')
                  if res[0] == 0:
                        return re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])', res[-1])

      @staticmethod
      def createLogger():
            logger = logging.getLogger('mylogger')
            logger.setLevel(logging.DEBUG)

            fh = logging.FileHandler('start_redis.log')
            fh.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(message)s')

            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            handlers = logger.__dict__.get('handlers')

            if len(handlers) < 2:
                  logger.addHandler(fh)
                  logger.addHandler(ch)

            return logger

      def loggerError(self, msg=''):
            if not msg:
                  self.logger.info(traceback.format_exc().replace('\n', '\t'))
            else:
                  self.logger.info(msg)

      def checkRedisMem(self, path=None):
            self.loggerError('%s check  maxmemory setting start' %self)
            if not path:
                  path = self.configPath
            file = os.path.join(path, 'redis_%s.conf' % str(self.port))
            if not os.path.isfile(file):
                  self.loggerError('%s  config file  %s not found' % (self, file))
                  return False

            try:
                  maxmem = None
                  with open(file, 'r') as f:
                        while 1:
                              data = f.readline()
                              if not data:
                                    break
                              if re.match(r'maxmemory\s+\d+\w', data.strip()):
                                    maxmem = re.findall(r'maxmemory\s+(\d+\w)', data.strip())[0]
                                    self.loggerError('%s found maxmemory config, value is %s' % (self, maxmem))
                                    break
                  if maxmem is None:
                        self.logger.info('%s check maxmemory setting done, not set maxmemory config' %self)
                        return False
                  if maxmem.lower() == self.maxmemory.lower():
                        self.logger.info('%s check maxmemory setting done, maxmemory equal maxmemory' %self)
                        return True

                  self.logger.info('%s check maxmemory setting done, maxmemory not equal maxmemory' %self)
                  return False
            except:
                  self.loggerError()

            return False

      def setRedisMem(self, path=None):
            if not path:
                  path = self.configPath

            file = os.path.join(path, 'redis_%s.conf' % str(self.port))
            if not os.path.isfile(file):
                  self.loggerError('%s  config file  %s not found' % (self, file))
                  return False

            try:
                  fold = open(file, 'r')
                  data = fold.readlines()
                  tempfile = str(int(time.time()))
                  abstempfile = os.path.join(path, tempfile)
                  with open(abstempfile, 'w') as f:
                        for item in data:
                              if re.match(r'maxmemory\s+\d+\w', item.strip()):
                              # if re.match(r'bind.*?\d+', item.strip()):
                                    item = '# ' + item
                              f.write(item)
                        f.write('maxmemory %s\n' % self.maxmemory)
                        f.flush()

                  os.rename(file, file + '.bak.' + str(int(time.time())))
                  self.loggerError('rename %s' % file)
                  os.rename(abstempfile, file)
                  self.loggerError('rename %s to %s' % (abstempfile, file))
                  return True
            except:
                  self.loggerError()
            return False

      def checkRedisAvailable(self):
            self.loggerError('%s check state start' %self)
            try:
                  r = StrictRedis(host=self.host, port=self.port, password=self.password)
                  if r.ping():
                        self.loggerError('%s check state done, redis is running' %self)
                        return True
            except:
                  self.loggerError('%s connect failed, try to use [ps aux|grep "redis-server"] to check state' %self)
                  return self.getPid()
                  # ret = self.execCmd('ps aux|grep "redis-server"')
                  # if not ret:
                  #       self.loggerError('%s check state done, not running' %self)
                  #       return False
                  # for item in ret:
                  #       if re.search(r'redis-server.*?:\d+', item):
                  #             port = int(re.findall(r'redis-server.*?:(\d+)', item)[0])
                  #             if port == self.port:
                  #                   self.loggerError('%s check state done, redis is running' %self)
                  #                   return True

            self.loggerError('%s check state done, not running' %self)
            return False

      def getPid(self):
            ret = self.execCmd('ps aux|grep redis-server')
            if not ret:
                  self.loggerError('%s check state done, not running' %self)
                  return ()
            try:
                  for item in ret:
                        if re.search(r'(.*?)\s+(\d+).*?redis-server.*?:(\d+)', item):
                              pidinfo =  re.search(r'(.*?)\s+(\d+).*?redis-server.*?:(\d+)', item).groups()
                              if self.port == int(pidinfo[-1]):
                                    self.loggerError('%s check state done, running user:%s, pid:%s' %(self, pidinfo[0], pidinfo[1]))
                                    return pidinfo
            except:
                  self.loggerError()

            self.loggerError('%s check state done, not running' %self)
            return ()

      def execCmd(self, cmd):
            res = commands.getstatusoutput(cmd)
            if res[0] == 0:
                  self.loggerError('%s execmd  %s success' %(self, cmd))
                  # self.loggerError(res[-1].split('\n'))
                  return res[-1].split('\n')
            self.loggerError('%s execmd  %s error %s' %(self, cmd, ' '.join(res[-1])))
            return None

      def start(self):
            if self.checkRedisAvailable():
                  self.loggerError('%s is running need not startup' %self)
                  return True

            if self.checkRedisMem():
                  self.loggerError('%s going to startup' %self)
                  ret = self.execCmd('redis-server %s' % os.path.join(self.configPath, 'redis_' + str(self.port) + '.conf'))
                  if ret:
                        self.loggerError('%s startup redis success' %self)
                        ret or self.loggerError('%s %s' % (self, ret))
                        return True
            self.loggerError('%s startup failed' % self)
            return False

      def stop(self):
            res = self.getPid()
            if res:
                  ret = self.execCmd('kill -9 %s' % res[1])
                  if ret:
                        self.loggerError('%s kill process pid: %s success' % (self, res[1]))
                        return True

            self.loggerError('%s kill process failed' % self)
            return False

      def __repr__(self):
            return '%s(host="%s", port=%s, maxmemory="%s")' %(self.__class__.__name__, self.host, self.port, self.maxmemory)


if __name__ == '__main__':
      ips = MyRedis.getAddr()
      print ips
      # nodes = filter(lambda x: x['host'] in ips, NODES)
      # for item in nodes:
      #       r = MyRedis(**item)
      #       r.stop()


