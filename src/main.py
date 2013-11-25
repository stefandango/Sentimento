import GetNewsPaperUrls
import cProfile, pstats, StringIO
from articletext import Articlescrape
from SentimentAnalysis import SentimentAnalysis
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

for newsPaper in newsPaperUrls.keys():
	urls = newsPaperUrls[newsPaper]
	text = ""

	for url in urls:
		try:
			print "url: " + url
			article = Articlescrape(url, configdict)
			textlist = article.gettextlist()
			date = article.getdate()
			print date
		except:
			print "Skipping url"
	print SA.moodscore(textlist)

#pr.disable()

#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()
