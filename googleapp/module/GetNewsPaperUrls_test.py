import unittest
from GetNewsPaperUrls import DownloadSubjectUrls

class GetNewsPaperUrlsTest(unittest.TestCase):
	
	def test_geturllist(self):
		EB = "ekstrabladet.dk"
		dsu = DownloadSubjectUrls([EB], "Scharf")
		urllist = dsu.geturllist()
		for site in urllist[EB]:
			self.assertTrue(EB in site)
		

if __name__ == '__main__':
	unittest.main()