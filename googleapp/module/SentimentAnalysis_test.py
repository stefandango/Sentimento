import unittest
from SentimentAnalysis import SentimentAnalysis

class SentimentAnalysisTest(unittest.TestCase):
	
	def test_SentimentAnalysis(self):
		sa = SentimentAnalysis();
		self.assertEqual(5.5, sa.moodscore(['xyz']))
		self.assertEqual(-3, sa.moodscore(['hader']))
		self.assertEqual(2, sa.moodscore(['elsker']))
		self.assertEqual(5.38, sa.moodscore(['hader', 'elsker', 'xyz']))
		

if __name__ == '__main__':
	unittest.main()