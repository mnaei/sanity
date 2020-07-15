from bottle import Bottle, run, request, static_file, HTTPResponse
from utils import Bid, Ask, Match, populateData, PriorityQueue
from collections import defaultdict
from threading import Timer
from time import time
import sys, json
import numpy as np


if "--dev" in sys.argv:

    # overide the original match class so that orders from the populateData
    # function are spread out over a random 20 second timeline
    class Match(Match):
        def __init__(self, time, price, amount):
            super().__init__(time, price, amount)
            self.time = int(time + np.random.rand() * 20)

    t = Timer(1, populateData)
    t.start()

app = Bottle()

global ASKID, BIDID
ASKID = 0
BIDID = 0

global ASKBOOK, BIDBOOK
ASKBOOK = PriorityQueue()
BIDBOOK = PriorityQueue()

global MATCHES
MATCHES = []

@app.get('/')
def home():
    return static_file("home.html", root = "")

@app.post('/buy')
def buy():
    global BIDID, BIDBOOK, ASKBOOK
    BIDID += 1
    gt = lambda lhs, rhs: lhs >= rhs
    return trade(BIDID, "buy", BIDBOOK, ASKBOOK, gt)

@app.post('/sell')
def sell():
    global ASKID, ASKBOOK, BIDBOOK
    ASKID += 1
    lt = lambda lhs, rhs: lhs <= rhs
    return trade(ASKID, "sell", ASKBOOK, BIDBOOK, lt)

def trade(id, side, book, crossedBook, cmp):
    global MATCHES
    price = request.POST.get("price")
    amount = request.POST.get("amount")
    price, amount = int(price), int(amount)

    while amount != 0 and not crossedBook.empty() and cmp(price, crossedBook.top().price):
        crossedOrder = crossedBook.top()
        if amount >= crossedOrder.amount:
            recordAmount = crossedOrder.amount
            amount -= crossedOrder.amount
            crossedBook.get()
        else:
            recordAmount = amount
            crossedOrder.amount -= amount
            amount = 0
        MATCHES.append(Match(time(), crossedOrder.price, recordAmount))

    if amount != 0:
        if side == "buy":
            book.put(Bid(id, price, amount))
        else:
            book.put(Ask(id, price, amount))

    return HTTPResponse(status=200)

@app.get('/display')
def display():
    global ASKBOOK, BIDBOOK
    askDisplay = defaultdict(int)
    bidDisplay = defaultdict(int)

    for order in ASKBOOK.queue:
        askDisplay[order.price] += order.amount

    for order in BIDBOOK.queue:
        bidDisplay[order.price] += order.amount

    askDisplay = sorted(askDisplay.items(), reverse=True)
    bidDisplay = sorted(bidDisplay.items(), reverse=True)

    return json.dumps({"asks": askDisplay, "bids": bidDisplay})

@app.get('/history')
def history():
    global MATCHES
    temp = defaultdict(list)
    chart = {}

    for m in MATCHES:
        temp[m.time].append(m)

    for k, v in temp.items():
        chart[k] = np.average([m.price for m in v], weights = [m.amount for m in v])

    return json.dumps(chart)


run(app, host='localhost', port=8080, debug=True, reloader=True, quiet=False)
