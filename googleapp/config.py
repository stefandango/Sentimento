MEDIADICT = {
			 "TV2": "nyhederne.tv2.dk", 
			 "EB": "ekstrabladet.dk",
			 "INF": "www.information.dk"}

MEDIALIST = [
			 {"id": "TV2", "display": "nyhederne.tv2.dk" },
			 {"id": "EB", "display": "ekstrabladet.dk" },
			 {"id":	"INF", "display": "www.information.dk"}]
		
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
							"extract": [("script", None), 
										("strong", None), 
										("div", "ads"), 
										("aside", "tools")]
						},
						"date": {
							"find": ("time", "page-timestamp"),
							"format": "%d. %B %Y, %H:%M"
						}
					},
				"www.information.dk":
					{
						"text": {
							"find": ("div", "field field-name-body"),
							"extract": [("a", None), ("b", None)]
						},
						"date": {
							"find":("span", "even"),
							"format": "%d. %B %Y"
						}

					}
			}

