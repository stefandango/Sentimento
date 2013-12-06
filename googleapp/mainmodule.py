#!/usr/bin/env python

# This file incudes all main functionality for downloading desired
# data and calculating the sentiment analysis

  
import StringIO
from collections import defaultdict
import re
import json
from threading import Thread, Lock
import Queue
import logging
import urlparse
import config
from datetime import datetime, date, time
from google.appengine.ext import ndb
from module import GetNewsPaperUrls
from module import articletext
from module import SentimentAnalysis

THREAD_LIMIT = 5
TASKS = Queue.Queue()
RESULTS = []

class Article(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    url = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    textlist = ndb.JsonProperty()

class Db():
	def putArticle(self, url, datetime, textlist):
		key = ndb.Key('ArticleStore', 'alpha')
		article = Article(parent=key)

		article.url = url
		article.date = datetime
		article.textlist = textlist
		article.put()
		logging.info("putted:" + article.url)

	def getArticle(self, url):
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
	The sentimentanalysismodule uses google to download a list og urls
	the content of each url are scraped based on the configeration file
	finally all data is processed through a text sentiment analysis
	"""

	def __init__(self, medialist, subject, startdate=None, enddate=None):
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
		"""

		#Get available urlx
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

		dividedwordlist = concatenation(RESULTS)

		alldata = textlisttosentiment(dividedwordlist)

		logging.info(json.dumps(alldata))

		return alldata


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
	Adds time as a key in the given dictionary
	returns the modified dictionary.
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