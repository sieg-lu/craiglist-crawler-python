# -*- coding: utf-8 -*-

'''
__author__ = 'http://www.cnblogs.com/nsnow/archive/2010/04/18/1714596.html'

import Queue
import threading
import sys
import time
import urllib

class my_thread(threading.Thread):
    def __init__(self, work_queue, result_queue, timeout=30, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.timeout = timeout
        self.setDaemon(True)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            try:
                callable, args, kwargs = self.work_queue.get(timeout=self.timeout)
                res = callable(args, kwargs)
                self.result_queue.put(res)
            except Queue.Empty:
                break
            except:
                print sys.exc_info()
                raise
    
class thread_pool:
    def __init__(self, num_of_threads=10):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []
        self.create_thread_pool(num_of_threads)

    def create_thread_pool(self, num_of_threads):
        for i in range(num_of_threads):
            thread = my_thread(self.work_queue, self.result_queue)
            self.threads.append(thread)

    def wait_for_complete(self):
        while len(self.threads):
            thread = self.threads.pop()
            if thread.isAlive():
                thread.join()
    
    def add_job(self, callable, *args, **kwargs):
        self.work_queue.put((callable, args, kwargs))


def test_job(id, sleep=0.001):
    html = ""
    try:
        conn = urllib.urlopen('http://www.google.com/')
        html = conn.read(20)
    except:
        print sys.exc_info()
    return html

def test():
    print 'start testing'
    tp = thread_pool(10)
    for i in range(50):
        tp.add_job(test_job, i, i*0.001)
    tp.wait_for_complete()

    print 'result Queue\'s length == %d '% tp.result_queue.qsize()
    while tp.result_queue.qsize():
        print tp.result_queue.get()
    print 'end testing'

# test()

'''
import Queue, threading, sys
from threading import Thread
import time,urllib
# working thread
class Worker(Thread):
   worker_count = 0
   def __init__( self, workQueue, resultQueue, timeout = 0, **kwds):
       Thread.__init__( self, **kwds )
       self.id = Worker.worker_count
       Worker.worker_count += 1
       self.setDaemon( True )
       self.workQueue = workQueue
       self.resultQueue = resultQueue
       self.timeout = timeout
       self.start( )
   def run( self ):
       ''' the get-some-work, do-some-work main loop of worker threads '''
       while True:
           try:
               callable, args, kwds = self.workQueue.get(timeout=self.timeout)
               res = callable(*args, **kwds)
               print "worker[%2d]: %s" % (self.id, str(res) )
               self.resultQueue.put( res )
           except Queue.Empty:
               break
           except :
               print 'worker[%2d]' % self.id, sys.exc_info()[:2]

class WorkerManager:
   def __init__( self, num_of_workers=10, timeout = 1):
       self.workQueue = Queue.Queue()
       self.resultQueue = Queue.Queue()
       self.workers = []
       self.timeout = timeout
       self._recruitThreads( num_of_workers )
   def _recruitThreads( self, num_of_workers ):
       for i in range( num_of_workers ):
           worker = Worker( self.workQueue, self.resultQueue, self.timeout )
           self.workers.append(worker)
   def wait_for_complete( self):
       # ...then, wait for each of them to terminate:
       while len(self.workers):
           worker = self.workers.pop()
           worker.join( )
           if worker.isAlive() and not self.workQueue.empty():
               self.workers.append( worker )
       print "All jobs are are completed."
   def add_job( self, callable, *args, **kwds ):
       self.workQueue.put( (callable, args, kwds) )
   def get_result( self, *args, **kwds ):
       return self.resultQueue.get( *args, **kwds )

def test_job(id, sleep = 0.001 ):
   try:
       urllib.urlopen('[url]https://www.gmail.com/[/url]').read()
   except:
       print '[%4d]' % id, sys.exc_info()[:2]
   return id

def test():
   import socket
   socket.setdefaulttimeout(10)
   print 'start testing'
   wm = WorkerManager(10)
   for i in range(500):
       wm.add_job( test_job, i, i*0.001 )
   wm.wait_for_complete()
   print 'end testing'

test()