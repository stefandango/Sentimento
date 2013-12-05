import unittest
import freqdist

class FrequencyDistributionTest(unittest.TestCase):
	
	def test_freqdist(self):
		f1 = freqdist.FrequencyDistribution("test1 test2 test3 test4 test5", 3)
		self.assertEqual(5, len(f1.distribution.items()))
		for item in f1.distribution.items():
			self.assertEqual(1, item[1])
		
		f2 = freqdist.FrequencyDistribution("test1 test2 test1 test1 test2", 3)
		self.assertEqual(2, len(f2.distribution.items()))
		self.assertEqual(3, f2.distribution.items()[0][1])
		self.assertEqual(2, f2.distribution.items()[1][1])

if __name__ == '__main__':
		unittest.main()