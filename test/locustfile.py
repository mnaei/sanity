from locust import HttpUser, task, between
import numpy as np


class QuickstartUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def index_page(self):
        side = np.random.choice(["sell", "buy"])
        price = int(np.random.randn() * 5 + 100)
        amount = int(np.random.rand() * 32)
        self.client.post("http://localhost:8080/" + side,
                         {"price": price, "amount": amount})
