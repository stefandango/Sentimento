#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
:mod:`GetNewsPaperUrls` -- News paper url module
====================================================

:synopsis: Search for article urls on a specified subject.
				Articles are found on article sites within a given time.

Requirements::
    1.  You need to install the google module from Mario Vilas, 
    	together with the jdcal module

"""


from google import search
import jdcal

# @TODO: move parameters to config file

def geturllistfromquery(query, amount=3):
	"""Performs a search on google.com and scrapes 
			the site for urls.

	The sets a mozilla firefox header for blocking reasons, but may be
	overwritten in a server setting.

	Args:
		amount (int) - the number of urls you want from a search

	Returns:
		(list) the result is a list of urls
	"""
	urls = []
	for url in search(query, tld='dk', lang='dk', 
							 		stop=amount, pause=0):
		urls.append(url)
	return urls 

def savetofile(filename, data):
	"""Save data to a local file.

	The list is saved to a file with one list item pr. 
		line in the file

	Args:
		data (list) - a list of strings
	"""

	current_file = open(filename.replace(".", "-") +".txt", "wb")
	for url in data:
		current_file.write(url + "\n")
	current_file.close()

def getjuliandate(inputdate):
	"""Converting a date object to the julian date format
	Args: 
		inputdate (datetime) - The date to covert

	Returns:
		(int) - The formattet julian date
	"""
	jdate = jdcal.gcal2jd(inputdate.year, inputdate.day, inputdate.month)
	return int(jdate[0] + jdate[1])

class DownloadSubjectUrls:
	"""Get urls to articles

	To find relevant urls three inputs are used; 
		Article sites, subject and time.
	We search for urls, from article sites, about a subject, 
		within a specified time bound.
	"""
	def __init__(self, medialist, subject):
		"""
		Args:
			medialist (list) - List of host names we want articles from
			subject (str) - the subject we are interested 
								in finding articles about
		"""
		self.medialist = medialist
		self.subject = subject


	def geturllist(self, startdate=None, enddate=None):
		"""Perform search and scrape, and get results as urls divided 
				by article/media sites

		Args: 
			startdate (datetime) - the beginning of the time bound 
			enddate (datetime) - the end of the time bound

		Returns:
			(dict) - keys are hostnames and values are a 
						list of resulting urls

		"""
		# If needed covert to julian date format
		startjulian = None
		endjulian = None

		if(startdate != None and enddate != None):
			startjulian = getjuliandate(startdate)
			endjulian = getjuliandate(enddate)

		# Perform search and construct dictionary
		mediadict = {}
		for media in self.medialist:
			if(startjulian != None and startjulian != None):
				urllist = geturllistfromquery("site:" + media + " " + self.subject + 
					" daterange:" + str(startjulian) + "-" + str(endjulian))
			else:
				urllist = geturllistfromquery("site:" + media + " " + self.subject)

			mediadict[media] = urllist

		return mediadict

if __name__ == "__main__":
    import sys
    args = sys.argv
    downloader = DownloadSubjectUrls(args[1], args[2])
    print downloader.geturllist()