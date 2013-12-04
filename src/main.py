import GetNewsPaperUrls
import cProfile, pstats, StringIO
import urlparse
from articletext import Articlescrape
from SentimentAnalysis import SentimentAnalysis
from multiprocessing import Pool
from collections import defaultdict
import re
import json

# For article text
configdict = { 
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

# From GetNewsPaperUrls.
MEDIALIST = ["nyhederne.tv2.dk", "ekstrabladet.dk"]
SUBJECT = "OL"
DOWNLOADER = GetNewsPaperUrls.DownloadSubjectUrls(MEDIALIST, SUBJECT)
SA = SentimentAnalysis()

#DOWNLOADER.geturllist(startdate, enddate)
#startdate = date(2001, 1, 1) enddate = date(2005, 12, 25)
newsPaperUrls = DOWNLOADER.geturllist()

#pr = cProfile.Profile()
#pr.enable()

#@TODO make a funktion or wrapper, to go through all urls without waiting
def fetchcontent(url):
	print "On it!"
	article = Articlescrape(url, configdict)
	textlist = article.gettextlist()
	date = article.getdate()
	print "Done: " + url
	return (url, textlist, date)

# Concanate text for newspapers
def concanate(contentList, granularity):
	""" 
	Input: 
		contentList: list of tuple in format (url, textlist, dateObj)
		granularity: "day", "week", "month", "year", "all"
	Output: Se below
	res = {
		eb.dk:{
			2021-12-31: ["...", "..."]
		},
		tv2:{

		}
	}
	Different formats for inner dict:
			all 	- "all": ["...", "..."] 
			year  	- 2012: ["...", "..."]
			month  	- 2012-12:["...", "..."]
			week 	- 2012-24:["...", "..."]
			day  	- 2012-12-24:["...", "..."]
	"""

	res = defaultdict(lambda: defaultdict(list))

	for content in contentlist:
		host = urlparse.urlparse(content[0]).hostname

		textlist = content[1]

		timetuple = content[2].timetuple()
		year = timetuple[0]
		month = timetuple[1]
		week = content[2].isocalendar()[1]
		day = timetuple[2]

		if granularity == "all":
			res[host]["all"] += textlist
		elif granularity == "year":
			res[host][year] += textlist
		elif granularity == "month":
			monthstr = str(year) + "-" + str(month)
			res[host][monthstr] += textlist
		elif granularity == "week":
			weekstr = str(year) + "-" + str(week)
			res[host][weekstr] += textlist
		elif granularity == "day":
			daystr = str(year) + "-" + str(month) + "-" + str(day)
			res[host][daystr] += textlist

	return res

def textlisttosentiment(dictionary):
	res = defaultdict(lambda: defaultdict(float))
	for paper in dictionary.keys():
		for time in dictionary[paper].keys():
			textlist = dictionary[paper][time]
			res[paper][time] = SA.moodscore(textlist)
	return res

# Create list of urls for queue
urls = []
for newsPaper in newsPaperUrls.keys():
	urls += newsPaperUrls[newsPaper]
print urls

# Get article text from all urls
pool = Pool(processes=10)
contentlist = pool.map(fetchcontent, urls)
print "contentlist"
print contentlist
granularity = "day";
paperText = concanate(contentlist, granularity)
print "paperText"
print paperText

paperSentiments = textlisttosentiment(paperText);
print "paperSentiments"
print json.dumps(paperSentiments)
#pr.disable()

#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
# print s.getvalue()
