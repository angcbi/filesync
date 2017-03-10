#!/usr/bin/env python
# encoding: utf-8

import os
import time
import pika
from multiprocessing import Pool, Process


def callback(ch, method, properties, body):
    print ' [x] Received %s, %s' %(os.getpid(), body,)
    time.sleep(body.count('.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def mycustom():
    conn = pika.BlockingConnection(pika.URLParameters('amqp://sampadm:sampadm123@127.0.0.1:5672'))
    channel = conn.channel()

    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='hello1')
    channel.start_consuming()

if __name__ == '__main__':
    print ' [*] waiting for messages. To exit press CTRL+C'
    p = Pool()
    for i in range(4):
        p.apply_async(mycustom)

    p.close()
    p.join()





