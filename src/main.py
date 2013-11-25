import GetNewsPaperUrls
import cProfile, pstats, StringIO
from articletext import Articlescrape
from SentimentAnalysis import SentimentAnalysis
from multiprocessing import Pool
import re

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
def testfunctionformultiprocessing(url):
    article = Articlescrape(url, configdict)
    textlist = article.gettextlist()

    return textlist

pool = Pool(processes=5)

for newsPaper in newsPaperUrls.keys():
	urls = newsPaperUrls[newsPaper]
	print urls
	print len(urls)
	text = ""

	l= pool.map(testfunctionformultiprocessing, urls)
	textlist = [item for sublist in l for item in sublist]

	print SA.moodscore(textlist)

#pr.disable()

#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()
