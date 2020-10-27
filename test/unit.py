import unittest
from boddle import boddle
from sanity import main


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        with boddle(params={"price": 100, "amount": 20}, path="/buy"):
            main.buy()
        with boddle(path="/display"):
            d = main.display()


if __name__ == '__main__':
    unittest.main()
