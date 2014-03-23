import time

def worker(q):
    while q.get:
        cmd = q.get()
        print cmd
        if cmd == 'end':
            print "end cmd reached"
            break
        time.sleep(1)   
    print "ending worker"

