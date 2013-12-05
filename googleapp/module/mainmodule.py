#!/usr/bin/env python

# This file incudes all main functionality for downloading desired
# data and calculating the sentiment analysis

import GetNewsPaperUrls
import StringIO
from articletext import Articlescrape
from SentimentAnalysis import SentimentAnalysis
from collections import defaultdict
import re
import json
from threading import Thread, Lock
import Queue
import logging
import urlparse

THREAD_LIMIT = 5
TASKS = Queue.Queue()
RESULTS = []
CONFIGDICT = { 
				"ekstrabladet.dk":
					{
						"text": {
							"find": ("div", "bodytext*"),
							"extract": [("a", None), ("b", None)]
						},
						"date": {	
							"find": ("span", "articletime"),
							"format": "%d. %B %Y kl. %H:%M"
						}
					},
				"nyhederne.tv2.dk":
					{
						"text": {
							"find": ("div", "page-body"),
							"extract": [("script", None), ("strong", None), ("div", "ads"), ("aside", "tools")]
						},
						"date": {
							"find": ("time", "page-timestamp"),
							"format": "%d. %B %Y, %H:%M"
						}
					}
			}

class sentimentanalysismodule():
	"""
	The sentimentanalysismodule uses google to download a list og urls
	the content of each url are scraped based on the configeration file
	finally all data is processed through a text sentiment analysis
	"""

	def __init__(self, medialist, subject, startdate=None, enddate=None):
		self.medialist = medialist
		self.subject = subject
		self.startdate = startdate
		self.enddate = enddate

	def startanalysis(self):
		"""
		Begins the class analysis. 
		"""
		#Get available urls
		downloader = GetNewsPaperUrls.DownloadSubjectUrls(self.medialist, self.subject)

		newspaperurls = downloader.geturllist()
		urllist = []
		for newspaper in newspaperurls.keys():
			urllist += newspaperurls[newspaper]

		for url in urllist:
			TASKS.put(url)

		for _ in range(THREAD_LIMIT):
			thread = Thread(target=fetchcontent)
			#thread.setDaemon(True)
			thread.start()

		TASKS.join()
		
		logging.info("data aquired.")

		dividedwordlist = concatenation(RESULTS)

		

		alldata = textlisttosentiment(dividedwordlist)

		logging.info(json.dumps(alldata))
		return json.dumps(alldata)


def concatenation(contentlist):
	"""
	concatenation takes a list of tubles containing url, text and date
	it splits text up based on its host and date. granularity of time is 
	divided into day, week, month, year and a total value.
	A dictionary containing all data is returned. 
	"""
	res = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

	for content in contentlist:

		#Get the host, the text data and the date for each article
		host = urlparse.urlparse(content[0]).hostname
		textlist = content[1]

		logging.info(host)
		"""
		timetuple = content[2].timetuple()

		#Split date into year, month, week, day
		year = timetuple[0]
		month = timetuple[1]
		week = content[2].isocalendar()[1]
		day = timetuple[2]
		"""
		#Total text of all host text
		res[host]["total"]["total"] += textlist
		"""
		#host text split into year
		res[host]["year"][year] += textlist

		#host text split into month
		monthstr = str(year) + "-" + str(month)
		res[host]["month"][monthstr] += textlist

		#host text split into week
		weekstr = str(year) + "-" + str(week)
		res[host][weekstr] += textlist

		#host text split into day
		daystr = str(year) + "-" + str(month) + "-" + str(day)
		res[host]["day"][daystr] += textlist
		"""
	return res


def textlisttosentiment(dictionary):
	"""
	Adds time as a key in the given dictionary
	returns the modified dictionary.
	"""
	res = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
	sentanalysis = SentimentAnalysis()
	for paper in dictionary.keys():
		for granularity in dictionary[paper].keys():
			for time in dictionary[paper][granularity].keys():
				textlist = dictionary[paper][granularity][time]
				res[paper][granularity][time] = sentanalysis.moodscore(textlist)
	return res

def fetchcontent():
	"""
	Defined as a worker background thread meant to speed up
	the process of downloading page content. 
	Adds the result of url, text and date to the RESULT list '
	as tuples. 
	"""
	while(1):
			try:
				task = TASKS.get(block=True)
				logging.info(task)

				article = Articlescrape(task, CONFIGDICT)
				textlist = article.gettextlist()
				#date = article.getdate()
				
				#RESULTS.put((task, textlist, date))
				RESULTS.append(((task, textlist)))

				if TASKS.empty() == True:
					break					
			finally:
				TASKS.task_done()
