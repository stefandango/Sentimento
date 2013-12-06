MEDIADICT = {"INF": "information.dk", 
			 "TV2": "nyhederne.tv2.dk", 
			 "EB": "ekstrabladet.dk",
			 "DR": "dr.dk"}

MEDIALIST = [{"id": "INF", "display": "information.dk" }, 
			 {"id": "TV2", "display": "nyhederne.tv2.dk" },
			 {"id": "EB", "display": "ekstrabladet.dk" },
			 {"id": "DR", "display": "dr.dk" }]
		
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
				"dr.dk/Nyheder":
					{
						"text": {
								"find": ("div", "wcms-article-content"),
								"extract": [("menu", "dr-site-share-horizontal"), 
											("menu", "dr-site-share"), 
											("div", "_dr-site-follow_"), 
											("style", None)]
						},
						"date": {
							"find": ("time", None),
							"format": "%d. %b %Y kl. %H:%M"
						}
					},
				"politiken.dk":
					{
					"text": {
							"find": ("div", "art-body"),
							"extract": [("b", None),
										("a", None)]
					},
					"date": {
						"find": ("time", None),
						"format": "%d. %b %Y KL. %H:%M"
					}
				}
			}

