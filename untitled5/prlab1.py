import threading
import time
def do_this():

    global  lock
    x=0

    lock.acquire() #acquires the lock (for locks or semaphores)
    try:
        while ( x<300 ):
            x += 1
            pass

        print(x)
    finally:
        lock.release() #releases the lock (for locks or semaphores)

def do_after():

    global   lock
    x=450
    lock.acquire()
    try:
        while ( x<600 ):
            x += 1
            pass
        time.sleep(0.1)#timer to track
        print(x)
    finally:
        lock.release()
def main():

    global x, lock, max_connections

    max_connections =5 #number of possible connections for semaphore(decreases from 5)
    #this chunk of code initalizes semaphore
    lock = threading.BoundedSemaphore(value=max_connections)
    #if you want to use locks instead of semaphore uncomment next section
    #lock=threading.Lock()
    #launches 4 threads and uses join
    for i in range(4):
        t = threading.Thread(target=do_this(), name=str(i))
        t.start()
        t.join()#releases the lock
        print(t.name)
        print(t.is_alive()) #checks if thread is alive, return True or False
    #launches another 6 threads without join
    for i in range(6):
        t = threading.Thread(target=do_after(), name=str(i))
        t.start()
        print(t.is_alive())
        print(t.name)




    input("Hit enter to stop the execution")
    dead = True #if thread is inactive return True



if (__name__ == "__main__"):
    main()