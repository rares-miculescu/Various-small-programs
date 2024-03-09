""" producer - consumer implementation"""
from random import randint
from threading import Semaphore, Lock, Thread
import time
import dataclasses

#types of coffe
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"

coffees = [ESPRESSO, AMERICANO, CAPPUCCINO]

#coffee sizes
SMALL = "small"
MEDIUM = "medium"
LARGE = "large"

sizes = [SMALL, MEDIUM, LARGE]

class Coffee:
    """ Base class """
    def __init__(self):
        self.type = randint(0, 2)
        self.size = randint(0, 2)

    def get_name(self):
        """ Returns the coffee name """
        return coffees[self.type]

    def get_size(self):
        """ Returns the coffee size """
        return sizes[self.size]

    @staticmethod
    def make_coffee():
        """generate coffee"""
        match type:
            case 0:
                return Espresso()
            case 1:
                return Americano()
            case _:
                return Cappuccino()

class Espresso (Coffee):
    """espresso class"""
    def __init__(self):
        super().__init__()

class Americano (Coffee):
    """americano class"""
    def __init__(self):
        super().__init__()

class Cappuccino (Coffee):
    """cappuccino class"""
    def __init__(self):
        super().__init__()

class Distributor:
    """ Distributor (buffer) class """
    def __init__(self):
        self.no_buffer = randint(2, 50)
        self.gol = Semaphore(value = self.no_buffer)
        self.plin = Semaphore(value = 0)
        self.mutex = Lock()
        self.buffer = []

class CoffeeFactory():
    """ Coffee Factory (producer) class """
    def __init__(self, distributor, index):
        self.id = index
        self.thread = Thread(target = CoffeeFactory.factory, args = (distributor, index))
        self.thread.start()

    def factory(distributor, index):
        while True:
            coffee = Coffee.make_coffee()
            time.sleep(randint(0, 2))
            distributor.gol.acquire()
            distributor.mutex.acquire()
            distributor.buffer.append(coffee)
            print("Factory " + str(index) + " produced a " +
                  coffee.get_size() + coffee.get_name())
            distributor.mutex.release()
            distributor.plin.release()

class User:
    """ User (consumer) class """
    def __init__(self, distributor, index):
        self.id = index
        self.thread = Thread(target = User.consumer, args = (distributor, index))
        self.thread.start()

    def consumer(distributor, index):
        while True:
            time.sleep(randint(0, 2))
            distributor.plin.acquire()
            distributor.mutex.acquire()
            coffee = distributor.buffer.pop()
            time.sleep(1)
            distributor.mutex.release()
            distributor.gol.release()
            print("Consumer " + str(index) + " consumed "
                  + coffee.get_name())


if __name__ == '__main__':
    distributor = Distributor()
    print("Buffer limit: " + str(distributor.no_buffer))

    #set the number of factories
    no_factories = randint(3, 50)
    print("Number of factories: " + str(no_factories))

    #create the factories
    factories = []
    for i in range(no_factories):
        factory = CoffeeFactory(distributor, i)
        factories.append(factory)

    #set the number of users
    no_users = randint(3, 50)
    print("Number of users: " + str(no_users))

    #create users
    users = []
    for i in range(no_users):
        user = User(distributor, i)
        users.append(user)

    for factory in factories:
        factory.thread.join()

    for user in users:
        user.thread.join()
