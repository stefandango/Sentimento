from google import search
import jdcal
from datetime import date, timedelta

# @TODO: move parameters to config file

def geturllistfromquery(query):
	"""
	docstring
	"""
	urls = []
	for url in search(query, tld='dk', lang='dk', stop=20, num=20, pause=0):
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
	def __init__(self, medialist, subject):
		self.medialist = medialist
		self.subject = subject

	def downloadtofiles(self):
		"""
		docstring
		"""

		for media in self.medialist:
			urllist = geturllistfromquery("site:" + media + " " + 
				daterange + self.subject)
			savetofile(media, urllist)
		return True

	def geturllist(self, startdate=None, enddate=None):
		"""
		docstring
		"""
		startjulian = None
		endjulian = None

		if(startdate != None and enddate != None):
			startjulian = getjuliandate(startdate)
			endjulian = getjuliandate(enddate)



		mediadict = {}
		for media in self.medialist:
			if(startjulian != None and startjulian != None):
				urllist = geturllistfromquery("site:" + media + " " + self.subject + 
					" daterange:" + str(startjulian) + "-" + str(endjulian))
			else:
				urllist = geturllistfromquery("site:" + media + " " + self.subject)
			
			mediadict[media] = urllist

		return mediadict

def getjuliandate(inputdate):
	jdate = jdcal.gcal2jd(inputdate.year, inputdate.day, inputdate.month)
	return int(jdate[0] + jdate[1])


