import multiprocessing
import time
import threading
from multiprocessing import Queue
from multiprocessing import Process
from workerBee import worker

q =  Queue()

q.put('hi')
q.put('hi')

worker = Process(target=worker, args = (q,))
worker.daemon = True
worker.start()

x = 0
while True:
    x += 1
    q.put(x)
    time.sleep(2)
    if x > 2:
        q.put('end')
        worker.join()
        print "worker has be collected"
        break


