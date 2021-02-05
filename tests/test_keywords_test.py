import unittest
from maio import keywordTrend as kt
class keywordsTest(unittest.TestCase):

    def setUp(self):
        self.trend = kt('쌍화차')
    def tearDown(self):
        del self.trend
    def test_keywords(self):
        results = self.trend.get_keywords(15)
        self.assertEqual(15,len(results))
        
if __name__ == '__main__':
    unittest.main()
