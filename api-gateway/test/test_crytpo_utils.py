import unittest
import sys
sys.path.append("../")
import json
import crypto_utils as cu
from sortedcontainers import SortedDict
from itertools import islice

class TestCrytpoUtils(unittest.TestCase):
    def test_top_assets(self):
        ranking = SortedDict()        
        ranking[1] = 'BTC'
        ranking[2] = 'ETH'
        
        pricing = dict()
        pricing['BTC'] = 10
        pricing['ETH'] = 5
        cache = dict()
        cache['ranking']= ranking
        cache['pricing'] = pricing

        u= cu.get_top_assets(10, cache)
        self.assertEqual(u[0]['rank'],1)
        
        self.assertEqual(u[0]['price'],10)

    def test_for_non_lexicografic_ordering(self):

        ranking = SortedDict()        
        ranking[1] = 'BTC'
        ranking[2] = 'ETH'
        ranking[3] = 'LTC'  
        ranking[10] = 'AAA'
        ranking[20] = 'BBB'

        pricing = dict()
        pricing['BTC'] = 10
        pricing['ETH'] = 5
        pricing['LTC'] = 2
        pricing['AAA'] = 0.1
        pricing['BBB'] = 0.01

        cache = dict()
        cache['ranking']= ranking
        cache['pricing'] = pricing

        u= cu.get_top_assets(10, cache)
        print(u)
        self.assertEqual(u[0]['symbol'],'BTC')
        self.assertEqual(u[1]['symbol'],'ETH')

    def test_null_pricing(self):

        ranking = SortedDict()        
        ranking[1] = 'BTC'
        ranking[2] = 'ETH'
        
        pricing = dict()
        pricing['BTC'] = 10
        cache = dict()
        cache['ranking']= ranking
        cache['pricing'] = pricing

        try:
            u= cu.get_top_assets(10, cache)
            self.assertEqual(u[1]['price'] , 'N/A')
        except ExceptionType:
            self.fail("get_top_assets raised exception")

    def test_null_ranking_value(self):

        ranking = SortedDict()        
        ranking[1] = 'BTC'
        
        pricing = dict()
        pricing['BTC'] = 10
        pricing['ETH'] = 5
        cache = dict()
        cache['ranking']= ranking
        cache['pricing'] = pricing

        try:
            u= cu.get_top_assets(10, cache)
            print(u)
        except ExceptionType:
            self.fail("get_top_assets raised exception")

    def test_null_ranking_cache(self):

        pricing = dict()
        pricing['BTC'] = 10
        pricing['ETH'] = 5
        cache = dict()
        cache['pricing'] = pricing
        cache['ranking']= None
        with self.assertRaises(Exception):

            u= cu.get_top_assets(10, cache)

if __name__ == '__main__':
    unittest.main()


