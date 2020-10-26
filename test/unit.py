# import unittest
from boddle import boddle
from sanity import main


def run():
    with boddle(params={"price": 100, "amount": 20}, path="/buy"):
        main.buy()
    with boddle(path="/display"):
        d = main.display()
        print(d)


run()

# class TestStringMethods(unittest.TestCase):

# def test_upper(self):
# with boddle(
# self.assertEqual('foo'.upper(), 'FOO')


# if __name__ == '__main__':
# unittest.main()
