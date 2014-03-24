from multiprocessing.connection import Listener
from array import array

address = ('localhost', 31415)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey='secret wavePi')
conn = listener.accept()
print 'connection accepted from', listener.last_accepted
while True:
    msg = conn.recv()
    # do something with msg
    if msg == 'close':
        conn.close()
        break
listener.close()