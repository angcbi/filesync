#!/usr/bin/env python
# encoding: utf-8

import sys
import pika
import time


message = ' '.join(sys.argv[1:]) or 'Hello, World'

conn = pika.BlockingConnection(pika.URLParameters('amqp://sampadm:sampadm123@127.0.0.1:5672'))
channel = conn.channel()
channel.queue_declare(queue='hello1', durable=True)

for i in xrange(1000):
    channel.basic_publish(exchange='', routing_key='hello1', body=message + str(i), properties=pika.BasicProperties(delivery_mode=2))
    time.sleep(0.5)
    print ' [x] Send %r' % (message,)
