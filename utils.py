import queue
import requests
import numpy as np

class PriorityQueue(queue.PriorityQueue):
    def top(self):
        return self.queue[0]

class Order():
    def __init__(self, id, price, amount):
        self.id = id
        self.price = price
        self.amount = amount

    def __str__(self):
        return f'({self.price}, {self.amount})'

    def __repr__(self):
        return f'({self.price}, {self.amount})'

class Ask(Order):
    def __lt__(self, rhs):
        if self.price == rhs.price:
            return self.id < rhs.id
        return self.price < rhs.price

class Bid(Order):
    def __lt__(self, rhs):
        if self.price == rhs.price:
            return self.id < rhs.id
        return self.price > rhs.price

class Match():
    def __init__(self, time, price, amount):
        self.time = int(time + np.random.rand() * 20) ## edit
        self.price = price
        self.amount = amount

    def __str__(self):
        return f'({self.time}, {self.price})'

    def __repr__(self):
        return f'({self.time}, {self.price})'

    def __lt__(self, rhs): ## edit
        return self.time < rhs.time

def populateData():
    size = 20

    side = np.random.choice(["sell", "buy"], size)
    price = (np.random.randn(size) * 5 + 100).astype(int)
    amount = (np.random.rand(size) * 32).astype(int)

    for i in range(size):
        requests.post("http://localhost:8080/" + side[i],
            {"price": price[i], "amount": amount[i]})
