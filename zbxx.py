# -*- coding:utf-8 -*-

import threading
from  lxml import html
import requests


class ZbxxError(Exception):
      pass


class ZBXX(threading.Thread):
      def __init__(self):
            self.base_url = 'www.hngp.gov.cn'
            self.url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=0&pageSize=50&pageNo=1'
            self.header = {
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Host': self.base_url,
            }
            self.res = []
            super(ZBXX, self).__init__()

      def get_page(self):
            try:
                  r = requests.get(url=self.url, headers=self.header, timeout=5)
                  if r.status_code != 200:
                        raise  ZbxxError('请求错误，错误码：%s' % r.status_code)
                  return r.text
            except Exception, e:
                  print e

      def parse_page(self, data):
            try:
                  page = html.fromstring(data)
                  res = page.xpath('//div[@class="List2"]/ul/li')
                  for item in res:
                        pub_date = item.xpath('./span/text()')[0] if len(item.xpath('./span/text()')) > 0 else None
                        url = item.xpath('./a/@href')[0] if item.xpath('./a/@href')[0] else None
                        title = item.xpath('./a/text()')[0] if len(item.xpath('./a/text()')[0]) > 0 else None
                        self.res.append({
                              'pub_date': pub_date,
                              'url': self.base_url + url,
                              'title': title
                        })
            except Exception, e:
                  print e

      def run(self):
            data = self.get_page()
            self.parse_page(data)


if __name__ == '__main__':
      p = ZBXX()
      p.run()
      for item in p.res:
            for k,v in item.iteritems():
                print '%s: %s\n' % (k, v)











































# import socket
# import select
# import Queue
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_address = ('', 8888)
# s.bind(server_address)
# s.listen(10)
# print '服务器启动成功, %s:%d...' %(server_address[0], server_address[1])
# s.setblocking(0)
# timeout = 10
# epoll = select.epoll()
# epoll.register(s.fileno(), select.EPOLLIN)
# message_queue = {}
# fd_to_socket = {s.fileno(): s}
#
# while True:
#       print '等待活动连接...'
#       events = epoll.poll(timeout)
#       if not events:
#             print 'epoll超时无活动连接，重巡轮训...'
#             continue
#       print '有', len(events), '个新事件，开始处理...'
#
#       for fd, event in events:
#             socket = fd_to_socket[fd]
#             if socket is s:
#                   connection, address = s.accept()
#                   print '来自%s:%d的新连接' %(address[0], address[1])
#                   connection.setblocking(0)
#                   epoll.register(connection.fileno(), select.EPOLLIN)
#                   fd_to_socket[connection.fileno()] = connection
#                   message_queue[connection] = Queue.Queue()
#             elif event & select.EPOLLHUP:
#                   print '客户端关闭'
#                   epoll.unregister(fd)
#                   fd_to_socket[fd].close()
#                   del fd_to_socket[fd]
#             elif event & select.EPOLLIN:
#                   data = socket.recv(1024)
#                   if data:
#                         print '接收到数据：', data, '客户端：', socket.getpeername()
#                         message_queue[socket].put(data)
#                         epoll.modify(fd, select.EPOLLOUT)
#             elif event & select.EPOLLOUT:
#                   try:
#                         msg = message_queue[socket].get_nowait()
#                   except Queue.Empty:
#                         print socket.getpeername(), " queue empty"
#                         epoll.modify(fd, select.EPOLLIN)
#                   else:
#                         print '发送数据： ', data, '客户端： ', socket.getpeername()
#                         socket.send(msg)
#
# epoll.unregister(s.fileno)
# epoll.close()
# s.close()

# import os
# import sys
# import re
# import time
# import threading
# from gevent.server import StreamServer
#
# def receive(sock, filename):
#       if os.path.exists(filename):
#             os.rename(filename, str(int(time.time())) + filename)
#       with open(filename, 'wb') as f:
#             total = 0
#             while 1:
#                   data = sock.recv(1024)
#                   total += len(data)
#                   sys.stdout.write(str(total) + '\r')
#                   sys.stdout.flush()
#                   f.write(data)
#                   if not data:
#                         break
#       print 'file receive done'
#       sock.close()
#
# def handle(sock, addr):
#       print 'New connection from %s:%d' %addr
#       sock.send('Hello from client\n')
#       while 1:
#             data = sock.recv(1024)
#             if not data:
#                   break
#             if data.startswith('file'):
#                   filename = os.path.split(data.split(' ')[-1])[-1]
#                   print 'receive file ', filename
#                   receive(sock, filename)
#
#       sock.close()
#
# s = StreamServer(('', 9999), handle=handle)
# s.serve_forever()







