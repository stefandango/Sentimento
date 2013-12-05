#!/usr/bin/env python

# This file incudes all main functionality for downloading desired
# data and calculating the sentiment analysis

import GetNewsPaperUrls
import cProfile, pstats, StringIO
import urlparse
from articletext import Articlescrape
from SentimentAnalysis import SentimentAnalysis
#from multiprocessing import Pool
from collections import defaultdict
import re
import json


#configdict = json.load(open('scrape/scrapeconfigeration.json'))
