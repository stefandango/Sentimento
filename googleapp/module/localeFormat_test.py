import unittest
import datetime
from localeFormat import LocaleFormat

class LocaleFormatTest(unittest.TestCase):
	
	def test_LocaleFormatAnalysis(self):
		lf = LocaleFormat()
		date = datetime.datetime.strptime("20. oct 2013, 18:43", "%d. %b %Y, %H:%M")
		self.assertEqual("20. oct 2013, 18:43", lf.localeFormat("20. Okt 2013, 18:43", "%d. %b %Y, %H:%M", "da_DK", "C"))
		self.assertEqual("20. october 2013, 18:43", lf.localeFormat("20. Oktober 2013, 18:43", "%d. %B %Y, %H:%M", "da_DK", "C"))
		self.assertEqual(date, lf.strptime("20. Oktober 2013, 18:43", "%d. %B %Y, %H:%M", "da_DK", "C"))
		

if __name__ == '__main__':
	unittest.main()