import unittest
from maio import keywordTrend as kt
class cdnsTest(unittest.TestCase):
    def setUp(self):
        self.trend = kt('쌍화차')
    def tearDown(self):
        del self.trend
    def test_coordinates(self):
        results = self.trend.kwds_coordinates()
        self.assertEqual(True,results != None)
        self.assertEqual(10,len(results))
if __name__ == '__main__':
    unittest.main()