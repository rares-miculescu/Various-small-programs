# CoffeeFactory - Users

Implement producer - consumer problem in Python, using classes, semaphores and locks.

### Classes:

    - Coffee: generate a coffee of random type and size
    - Espresso: subclass of Coffee
    - Americano: subclass of Coffee
    - Cappuccino: subclass of Coffee
    - Distributor: 
        - middleman for consumer and producer
        - have semaphores and buffer
    - CoffeeFactory: produce coffees and give to distributor
    - User: get coffee from distributor and consume
