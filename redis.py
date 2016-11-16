#!/usr/bin/env python
# encoding: utf-8

import urlparse
from io import StringIO
import socket
import warnings


class SocketBuffer(object):
      def __init__(self, sock, sock_read_size):
            self.sock_read_size = sock_read_size
            self._sock = sock
            self._buf = StringIO()
            self.buf_written = 0
            self.buf_read = 0

      @property
      def length(self):
            return self.buf_written - self.buf_read

      def _read_from_socket(self, length=None):
            try:
                  buffer = self._buf
                  buffer.seek(self.buf_written)
                  socket_read_size = self.sock_read_size
                  marker = 0

                  while 1:
                        data = self._sock.recv(socket_read_size)
                        if isinstance(data, str) and len(data) == 0:
                              raise EnvironmentError("Socket error")
                        buffer.write(data.decode('utf8'))
                        self.buf_written += len(data)
                        marker += len(data)

                        if length is not None and marker < length:
                              continue
                        break
            except Exception, e:
                  print e


      def readline(self):
            self._buf.seek(self.buf_read)
            data = self._buf.readline()

            while not data.endswith('\r\n'):
                  self._read_from_socket()
                  self._buf.seek(self.buf_read)
                  data = self._buf.readline()

            self.buf_read += len(data)
            if self.buf_read == self.buf_written:
                  self.purget()

            return data[:-2]

      def read(self, length):
            length = length + 2
            if length > self.length:
                  self._read_from_socket(length - self.length)

            self._buf.seek(self.buf_read)
            data = self._buf.read(length)
            self.buf_read += length

            if self.buf_read == self.buf_written:
                  self.purget()

            return data[:-2]


      def purget(self):
            self._buf.seek(0)
            self._buf.truncate()
            self.buf_read = 0
            self.buf_written = 0

      def close(self):
            try:
                  self.purget()
                  self._buf.close()
            except:
                  pass
            self._sock = None
            self._buf = None

class PythonParse(object):
      def __init__(self, sock, sock_read_size):
            self._sock = sock
            self._buffer = SocketBuffer(self._sock, sock_read_size)

      def can_read(self):
            return self._buf and bool(self._buf.length)

      def read_response(self):
            response = self._buffer.readline()
            if not response:
                  raise Exception("1111")
            byte, response = response[0], response[1:]
            if byte not in ('*', '-', '$', '+', ':'):
                  raise Exception("Protocol Error: %s, %s" % (byte, response))

            if byte == '+':
                  pass
            elif byte == '-':
                  pass
            elif byte == ':':
                  response = long(response)
            elif byte == '$':
                  length = long(response)
                  if length == -1:
                        return None
                  response = self._buffer.read(length)
            elif byte == '*':
                  length = long(response)
                  response = [self.read_response() for i in xrange(length)]

            return response


class Redis(object):
      def __init__(self, host='192.168.1.36', port=6379, db=0, password=None, encoding='utf-8', sock_read_size=4096*4):
            try:
                  self.s = socket.create_connection((host, port), timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
                  self.parse = PythonParse(self.s, sock_read_size)
                  if password:
                        res = self.exec_command('AUTH', password)
                        if res != 'OK':
                              raise  Exception(res)
                  if db:
                        res1 =  self.exec_command('SELECT', db)
                        if res1 != 'OK':
                              raise  Exception(res1)
            except Exception, e:
                  print e

      @classmethod
      def from_url(cls, url):
            qs = urlparse.urlparse(url)
            qs_dict = {
                  'host': qs.hostname or '192.168.1.36',
                  'password': qs.password or 'None',
                  'port': qs.port or 6379,
                  'db': int(qs.path.replace('/', '')),
            }

            return cls(**qs_dict)

      def exec_command(self, *args, **kwargs):
            templist = map(str, list(args))
            if kwargs:
                  for item in kwargs.iteritems():
                        templist.extend(map(str, item))
            if templist:
                  templist[-1] = templist[-1] + '\r\n'
            # print repr(' '.join(templist))
            self.s.sendall(' '.join(templist))
            return self.parse.read_response()

      # def parse_data(self, data):
      #       try:
      #             if data:
      #                   if data.startswith('+'):
      #                         if data.split('\r\n')[0][1:].upper() == 'OK':
      #                               return True
      #                         return False
      #                   elif data.startswith('-'):
      #                         raise Exception(data[1:])
      #                   elif data.startswith(':'):
      #                         return data.strip().split('\r\n')[0][1:]
      #                   elif data.startswith('*'):
      #                         return self.parse_start_star(data)
      #                   elif data.startswith('$'):
      #                         try:
      #                               tl = data.strip().split('\r\n')
      #                               for i in range(len(tl)):
      #                                     if tl[i].startswith('$'):
      #                                           length = int(tl[i][1:])
      #                                           if length < 0:
      #                                                 return None
      #                                           return tl[i+1][0:int(tl[i][1:])]
      #                         except Exception, e:
      #                               print e
      #                               return None
      #                   else:
      #                         pass
      #       except Exception, e:
      #             print e
      #             return None
      #
      # def parse_start_star(self, data):
      #       res = []
      #       templist = data.strip().split('\r\n')
      #       totallines = int(templist[0][1:])
      #       for i in range(1, len(templist)):
      #             if templist[i].startswith('$'):
      #                   length = int(templist[i][1:])
      #                   res.append(templist[i+1][:length])
      #       return res


      def set(self, key, value):
            return self.exec_command('set', key, value)

      def get(self, key):
            return self.exec_command('get', key)

      def incr(self, key):
            return self.exec_command('incr', key)

      def mset(self, *args, **kwargs):
            for item in args:
                  if isinstance(item, dict):
                        kwargs.update(item)
            return self.exec_command('mset', **kwargs)

      def mget(self, *args):
            return self.exec_command('mget', *args)

      def delete(self, key):
            return self.exec_command('del', key)

      def lpush(self, key, *args):
            return self.exec_command('lpush', key, *args)

      def lrange(self, key, start, end):
            return self.exec_command('lrange', key, start, end)

      def lpop(self, key):
            return self.exec_command('lpop', key)

      def rpop(self, key):
            return self.exec_command('rpop', key)

      def ltrim(self, key, start, end):
            return self.exec_command('ltrim', key, start, end)

      def llen(self, key):
            return self.exec_command('llen', key)

      def keys(self, key=None):
            if not key:
                  key = '*'
            return self.exec_command('keys',key)

      def sadd(self, key, *args):
            return self.exec_command('sadd', key, *args)

      def smembers(self, key):
            return self.exec_command('smembers', key)

      def spop(self, key):
            return self.exec_command('spop', key)

      def hmset(self, key, *args, **kwargs):
            for item in args:
                  if isinstance(item, dict):
                        kwargs.update(item)
            return self.exec_command('hmset', key, **kwargs)


if __name__ == '__main__':
      r = Redis(db=1)
      print r.keys()