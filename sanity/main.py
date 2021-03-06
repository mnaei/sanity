from bottle import Bottle, run, request, static_file, HTTPResponse
from sanity.utils import Bid, Ask, Match, populateData
from heapq import heappush, heappop
from collections import defaultdict
from threading import Timer, Lock
from time import time
import numpy as np
import sys
import json


if "--dev" in sys.argv:
    # overide the original match class so that orders from the populateData
    # function are spread out over a random 20 second timeline
    class Match(Match):  # pylint: disable=E0102,R0903
        def __init__(self, time_, price, amount):
            super().__init__(time_, price, amount)
            self.time = int(time_ + np.random.rand() * 20)

    t = Timer(5, populateData)
    t.start()

app = Bottle()

global ASKID, BIDID  # pylint: disable=W0604
ASKID = 0
BIDID = 0

global ASKBOOK, BIDBOOK, MATCHES  # pylint: disable=W0604
ASKBOOK = []
BIDBOOK = []
MATCHES = []

global bidLock, askLock, matchingLock  # pylint: disable=W0604
bidLock = Lock()
askLock = Lock()
matchingLock = Lock()


@app.get('/')
def home():
    return static_file("home.html", root="")


@app.post('/buy')
def buy():
    global BIDID, BIDBOOK, ASKBOOK, bidLock  # pylint: disable=W0603
    with bidLock:
        BIDID += 1
        id_ = BIDID

    def gt(lhs, rhs): return lhs >= rhs
    return trade(id_, "buy", BIDBOOK, ASKBOOK, gt)


@app.post('/sell')
def sell():
    global ASKID, ASKBOOK, BIDBOOK, askLock  # pylint: disable=W0603
    with askLock:
        ASKID += 1
        id_ = ASKID

    def lt(lhs, rhs): return lhs <= rhs
    return trade(id_, "sell", ASKBOOK, BIDBOOK, lt)


def trade(id_, side, book, crossedBook, cmp):
    global MATCHES, matchingLock  # pylint: disable=W0603
    price = request.POST.get("price")  # pylint: disable=E1101
    amount = request.POST.get("amount")  # pylint: disable=E1101
    price, amount = int(price), int(amount)

    with matchingLock:
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
            MATCHES.append(Match(time(), crossedOrder.price, recordAmount))

        if amount:
            if side == "buy":
                heappush(book, Bid(id_, price, amount))
            else:
                heappush(book, Ask(id_, price, amount))

    return HTTPResponse(status=200)


@app.get('/display')
def display():
    global ASKBOOK, BIDBOOK, matchingLock  # pylint: disable=W0603
    askDisplay = defaultdict(int)
    bidDisplay = defaultdict(int)

    with matchingLock:
        for order in ASKBOOK:
            askDisplay[order.price] += order.amount

        for order in BIDBOOK:
            bidDisplay[order.price] += order.amount

    askDisplay = sorted(askDisplay.items(), reverse=True)
    bidDisplay = sorted(bidDisplay.items(), reverse=True)

    return json.dumps({"asks": askDisplay, "bids": bidDisplay})


@app.get('/history')
def history():
    global MATCHES, matchingLock  # pylint: disable=W0603
    temp = defaultdict(list)
    chart = {}

    with matchingLock:
        for m in MATCHES:
            temp[m.time].append(m)

    for k, v in temp.items():
        chart[k] = np.average([m.price for m in v],
                              weights=[m.amount for m in v])

    return json.dumps(chart)


if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=False,
        quiet=True, reloader=True, server="paste")
