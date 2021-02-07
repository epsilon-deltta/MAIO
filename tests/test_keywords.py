import unittest
from maio import keywordTrend as kt
class keywordsTest(unittest.TestCase):

    def setUp(self):
        self.trend = kt('쌍화차')
    def tearDown(self):
        del self.trend
    def test_keywords(self):
        self.trend.set_keyword('쌍화차')
        results = self.trend.get_keywords(15)
        self.assertEqual(15,len(results))

    def test_set_keyword(self):
        nokey = '영화 아이언맨'
        self.trend.set_keyword(nokey)

        self.assertEqual(None,self.trend.tkwds )
        self.assertEqual(None,self.trend.kwds_coordis)
        
if __name__ == '__main__':
    unittest.main()
