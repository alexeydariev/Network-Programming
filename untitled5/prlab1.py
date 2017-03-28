import threading
import time


def count():

    global x, lock, maxconnections
    #maxconnections = 4
    x=0

    lock.acquire()
    try:
        while(x<300):
            x+=1
            pass
        print(x)
    finally:
        lock.release()

def main():
    global x, lock
    maxconnections = 2
    lock = threading.Lock()


    thread1=threading.Thread(target=count)
    thread1.start()
    thread2 = threading.Thread(target=count)
    thread3 = threading.Thread(target=count)
    thread4 = threading.Thread(target=count)
    thread5 = threading.Thread(target=count)
    thread6 = threading.Thread(target=count)
    thread7 = threading.Thread(target=count)


    if thread1.is_alive() == False:
        thread2.start()

        thread3.start()

        thread4.start()

    if thread2.is_alive() == False:
        print( "thread2 finished its process")
        thread5.start()


    if thread3.is_alive()== False:
        print("thread3 finished its process")
        thread6.start()

    if thread4.is_alive()==False:
        print("thread4 finished its process")
        thread7.start()



if (__name__ == "__main__"):
    main()