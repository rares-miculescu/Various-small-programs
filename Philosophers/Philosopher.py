from random import randint
from threading import Lock, Thread
import time

n = randint(5, 10)
print("Number of philosophers: " + str(n))

forks = []
philosophers = []

class Fork:
    """fork class"""
    def __init__(self):
        self.lock = Lock()

class Philosopher:
    """philosopher class"""
    def __init__(self, index):
        self.id = index
        self.thread = Thread(target = Philosopher.eat, args = (self.id,))
        self.thread.start()

    def eat(id):
        while(True):
            if id != n - 1:
                tm = time.sleep(randint(0, 5))
                forks[id].lock.acquire()
                forks[id + 1].lock.acquire()
                print("Philosopher " + str(id) + " eats")
                time.sleep(randint(0, 3))
                print("Philosopher " + str(id) + " finished eating")
                forks[id].lock.release()
                forks[id + 1].lock.release()
            else:
                tm = time.sleep(randint(0, 5))
                forks[0].lock.acquire()
                forks[n - 1].lock.acquire()
                print("Philosopher " + str(id) + " eats")
                time.sleep(randint(0, 3))
                print("Philosopher " + str(id) + " finished eating")
                forks[0].lock.release()
                forks[n - 1].lock.release()

if __name__ == '__main__':

    #create forks
    for i in range(n):
        fork = Fork()
        forks.append(fork)
    
    #create philosophers
    for i in range(n):
        philosopher = Philosopher(i)
        philosophers.append(philosopher)

    for philosopher in philosophers:
        philosopher.thread.join()
