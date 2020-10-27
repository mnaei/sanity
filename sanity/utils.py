import requests
import numpy as np


class Order():
    def __init__(self, id_, price, amount):
        self.id = id_
        self.price = price
        self.amount = amount

    def __eq__(self, other):
        return self.id == other.id and self.price == other.price and self.amount == other.amount

    def __str__(self):
        return f'({self.price}, {self.amount})'

    def __repr__(self):
        return f'({self.price}, {self.amount})'


class Ask(Order):  # pylint: disable=R0903
    def __lt__(self, rhs):
        if self.price == rhs.price:
            return self.id < rhs.id
        return self.price < rhs.price


class Bid(Order):  # pylint: disable=R0903
    def __lt__(self, rhs):
        if self.price == rhs.price:
            return self.id < rhs.id
        return self.price > rhs.price


class Match():
    def __init__(self, time, price, amount):
        self.time = int(time)
        self.price = price
        self.amount = amount

    def __str__(self):
        return f'({self.time}, {self.price})'

    def __repr__(self):
        return f'({self.time}, {self.price})'

    def __lt__(self, rhs):  # edit
        return self.time < rhs.time
