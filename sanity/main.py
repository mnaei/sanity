from sanity.utils import Bid, Ask, Match
from heapq import heappush, heappop
from collections import defaultdict
from threading import Lock
from time import time
import numpy as np
import json


class MatchingEngine:

    def __init__(self):

        self.ASKID = 0
        self.BIDID = 0

        self.ASKBOOK = []
        self.BIDBOOK = []
        self.MATCHES = []

        self.bidLock = Lock()
        self.askLock = Lock()
        self.matchingLock = Lock()

    def buy(self, price, amount):
        with self.bidLock:
            self.BIDID += 1
            id_ = self.BIDID

        def gt(lhs, rhs): return lhs >= rhs
        self.trade(id_, price, amount, "buy", self.BIDBOOK, self.ASKBOOK, gt)

    def sell(self, price, amount):
        with self.askLock:
            self.ASKID += 1
            id_ = self.ASKID

        def lt(lhs, rhs): return lhs <= rhs
        self.trade(id_, price, amount, "sell", self.ASKBOOK, self.BIDBOOK, lt)

    def trade(self, id_, price, amount, side, book, crossedBook, cmp):

        with self.matchingLock:
            while amount and crossedBook and cmp(price, crossedBook[0].price):
                crossedOrder = crossedBook[0]
                if amount >= crossedOrder.amount:
                    recordAmount = crossedOrder.amount
                    amount -= crossedOrder.amount
                    heappop(crossedBook)
                else:
                    recordAmount = amount
                    crossedOrder.amount -= amount
                    amount = 0
                self.MATCHES.append(
                    Match(time(), crossedOrder.price, recordAmount))

            if amount:
                if side == "buy":
                    heappush(book, Bid(id_, price, amount))
                else:
                    heappush(book, Ask(id_, price, amount))

    def display(self):
        askDisplay = defaultdict(int)
        bidDisplay = defaultdict(int)

        with self.matchingLock:
            for order in self.ASKBOOK:
                askDisplay[order.price] += order.amount

            for order in self.BIDBOOK:
                bidDisplay[order.price] += order.amount

        askDisplay = sorted(askDisplay.items(), reverse=True)
        bidDisplay = sorted(bidDisplay.items(), reverse=True)

        return json.dumps({"asks": askDisplay, "bids": bidDisplay})

    def history(self):
        temp = defaultdict(list)
        chart = {}

        with self.matchingLock:
            for m in self.MATCHES:
                temp[m.time].append(m)

        for k, v in temp.items():
            chart[k] = np.average([m.price for m in v],
                                  weights=[m.amount for m in v])

        return json.dumps(chart)
