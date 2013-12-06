#!/usr/bin/env python

# This file incudes all main functionality for downloading desired
# data and calculating the sentiment analysis

"""
:mod:`mainmodule` -- incudes all main functionality for 
			downloading desired data and calculating the sentiment analysis.
============================================================================

:synopsis: Fetches the body text from online articles.

Requirements::
    1.  Run the code in an 2.7 environment
"""

__version__ = 1.00
__author__ = "Group 21"
__all__ = ["mainmodule"]

import StringIO
from collections import defaultdict
import re
import json
from threading import Thread, Lock
import Queue
import logging
import urlparse
from datetime import datetime, date, time
from google.appengine.ext import ndb
from module import GetNewsPaperUrls
from module import articletext
from module import SentimentAnalysis

THREAD_LIMIT = 5
TASKS = Queue.Queue()
RESULTS = []

class Article(ndb.Model):
	"""
	Defines an entry in the database.
	"""
	url = ndb.StringProperty()
	date = ndb.DateTimeProperty()
	textlist = ndb.JsonProperty()

class Db():
	"""
	Handles commands and queries to the database.
	"""
	def putArticle(self, url, datetime, textlist):
		"""
		Adds a new entry to the database.
		
		Args:
			url (str) - The URL to the article
			datetime (datetime) - The date (if any) that the article was published.
			textlist (list) - The contents of the body text, of the article.
		"""
		key = ndb.Key('ArticleStore', 'alpha')
		article = Article(parent=key)

		article.url = url
		article.date = datetime
		article.textlist = textlist
		article.put()
		logging.info("putted:" + article.url)

	def getArticle(self, url):
		"""
		Queries the database for an entry.
		
		Args:
			url (str) - The URL to the article, that is to be used for the query.
			
		Returns:
			article (Article) - The article object that was stored in the database.
								If the article isn't found, None is returned.
		"""
		articles_query = Article.query(Article.url == url)
		articles = articles_query.fetch(1)
		logging.info(articles)
		if not articles:
			return None
		else:
			article = articles[0]
			logging.info("read:" + article.url)
			return article

class sentimentanalysismodule():
	"""
	Performs online searches for articles for a given subject, and
	computes a sentiment analysis 'score' for the articles.
	"""
	
	def __init__(self, medialist, subject, startdate=None, enddate=None):
		"""
		Kwargs:
			medialist (list) - A list of the hostnames to be searched for articles.
			subject (str) - The subject to search for
			startdate (datetime) - If provided, the search will return articles after this date.
			enddate (datetime) - If provided, the search will return articles before this date.
		"""
		
		self.medialist = medialist
		
		badchars = ['<','>','\"','\'','\\','/',';',':','!','?']
		for badchar in badchars:
			subject = subject.replace(badchar, '')
		
		self.subject = subject
		self.startdate = startdate
		self.enddate = enddate
		global TASKS
		global RESULTS
		TASKS = Queue.Queue()
		RESULTS = []

	def startanalysis(self):
		"""
		Begins the class analysis. 
		
		Returns:
			(json) - A json object containing the results of the sentiment analysis.
		"""
		
		downloader = GetNewsPaperUrls.DownloadSubjectUrls(self.medialist, self.subject)
		newspaperurls = downloader.geturllist()

		logging.info(newspaperurls)
		for newspaper in newspaperurls.keys():
			for url in newspaperurls[newspaper]:
				TASKS.put(url)

		for _ in range(THREAD_LIMIT):
			thread = Thread(target=fetchcontent)
			thread.start()

		TASKS.join()
		
		logging.info("data aquired.")

		dividedwordlist = parsedata(RESULTS)

		alldata = textlisttosentiment(dividedwordlist)

		logging.info(json.dumps(alldata))

		return alldata


def parsedata(contentlist):
	"""
	parsedata takes a list of tubles containing url, text and date
	it splits text up based on its host and date. granularity of time is 
	divided into day, week, month, year and a total value.
	A dictionary containing all data is returned. 
	
	Args:
		contentlist (list) - The list of tuples to process.
	
	Returns:
		res (dict) - A three-dimentional dictionary, containing the result of the processing.
	"""
	res = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

	for content in contentlist:

		#Get the host, the text data and the date for each article
		host = urlparse.urlparse(content[0]).hostname
		textlist = content[1]

		if(content[2] == None):
			continue
		timetuple = content[2].timetuple()

		#Split date into year, month, week, day
		year = timetuple[0]
		month = timetuple[1]
		week = content[2].isocalendar()[1]
		day = timetuple[2]
		
		#Total text of all host text
		res["total"][host]["total"] += textlist
		
		#host text split into year
		res["year"][host][year] += textlist

		#host text split into month
		monthstr = str(year) + "-" + str(month)
		res["month"][host][monthstr] += textlist

		#host text split into week
		weekstr = str(year) + "-" + str(week)
		res["week"][host][weekstr] += textlist

		#host text split into day
		daystr = str(year) + "-" + str(month) + "-" + str(day)
		res["day"][host][daystr] += textlist
		
	return res


def textlisttosentiment(dictionary):
	"""
	Replaces text by sentiment score in dictionary.
	
	Args:
		dictionary (dict) - A dictionary with article texts.
		
	Returns:
		dictionary (dict) - The modified version of the input dictionary.
	"""
	
	res = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
	sentanalysis = SentimentAnalysis.SentimentAnalysis()
	for granularity in dictionary.keys():
		for paper in dictionary[granularity].keys():
			for time in dictionary[granularity][paper].keys():
				textlist = dictionary[granularity][paper][time]
				res[granularity][paper][time] = sentanalysis.moodscore(textlist)
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
				date = None
				textlist = []
				db = Db()
				article = db.getArticle(task)

				if(article != None):
					textlist = article.textlist
					date = article.date
					
				else:
					article = articletext.Articlescrape(task, CONFIGDICT)
					textlist = article.gettextlist()
					date = article.getdate()
					db.putArticle(task, date, textlist)
				
				RESULTS.append(((task, textlist, date)))
				if TASKS.empty() == True:
					break

			finally:
				TASKS.task_done()

if __name__ == "__main__":
	import sys
	args = sys.argv
	medialist = args[1]
	subject = args[2]
	startdate = args[3]
	enddate = args[4]
	
	articlescrape = sentimentanalysismodule(self, medialist, subject, startdate=None, enddate=None)
	