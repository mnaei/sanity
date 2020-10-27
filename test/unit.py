import unittest
from sanity.main import MatchingEngine
from sanity.utils import Bid, Ask, Match


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        engine = MatchingEngine()
        engine.buy(100, 20)
        bid = Bid(1, 100, 20)
        breakpoint()
        self.assertIn(bid, engine.BIDBOOK)


if __name__ == '__main__':
    unittest.main()
