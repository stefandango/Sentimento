from google import search
#import jdcal
from datetime import date, timedelta

# @TODO: move parameters to config file

def geturllistfromquery(query):
	"""
	docstring
	"""
	urls = []
	for url in search(query, tld='dk', lang='dk', stop=5, pause=0):
		urls.append(url)
	return urls 

def savetofile(filename, data):
	"""
	docstring
	"""

	current_file = open(filename.replace(".", "-") +".txt", "wb")
	for url in data:
		current_file.write(url + "\n")
	current_file.close()

class DownloadSubjectUrls:
	"""
	docstring
	"""
	def __init__(self, medialist, subject, daysAgo=None):
		self.medialist = medialist
		self.subject = subject
		self.daysAgo = daysAgo

	def downloadtofiles(self):
		"""
		docstring
		"""
		daterange = ""

		"""
		if (self.daysAgo != None):
			daterange = "daterange:" + str(self.getjuliandate()) + "-" + 
			str(self.getjuliandate(self.daysAgo)) + " "
			print daterange
		"""
		for media in self.medialist:
			urllist = geturllistfromquery("site:" + media + " " + 
				daterange + self.subject)
			savetofile(media, urllist)
		return True

	def geturllist(self):
		"""
		docstring
		"""
		mediadict = {}
		for media in self.medialist:
			urllist = geturllistfromquery("site:" + media + " " + self.subject)
			mediadict[media] = urllist

		return mediadict
"""
	def getjuliandate(self, daystosubtract=0):
		actualdate=date.today()-timedelta(days=daystosubtract)
		print actualdate
		jdate = jdcal.gcal2jd(actualdate.year, actualdate.day, actualdate.month)
		return int(jdate[0] + jdate[1])
"""

"""
Moved to main.py:

MEDIALIST = ["ekstrabladet.dk", "politiken.dk"]
SUBJECT = "Helle Thorning Smidt"
DOWNLOADER = DownloadSubjectUrls(MEDIALIST, SUBJECT, 3)
print DOWNLOADER.geturllist()
"""
