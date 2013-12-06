import unittest
import articletext

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

class ArticletextTest(unittest.TestCase):

	def test_articletext(self):
		url = "http://ekstrabladet.dk/nyheder/politik/article2165388.ece"
		words_from_article = ["GGGI", "regnskaber", "Udenrigsministeriet", "skeletterne", "Folketinget", "modregnet"]
		artscrape = articletext.Articlescrape(url, CONFIGDICT)
		textlist = artscrape.gettextlist()
		
		for articleword in words_from_article:
			self.assertTrue(articleword in textlist)

if __name__ == '__main__':
	unittest.main()