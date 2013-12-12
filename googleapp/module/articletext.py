#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:mod:`articletext` -- Fetches the body text from online articles
================================================================

:synopsis: Fetches the body text from online articles.

Requirements::
    1.  Run the code in an 2.7 environment
"""

import urllib2
import urlparse
import re
from BeautifulSoup import BeautifulSoup
from localeFormat import LocaleFormat
import logging

__version__ = 1.00
__author__ = "Group 21"
__all__ = ["articletext"]

class Articlescrape:
	"""Fetches the body text from online articles."""
	def __init__(self, url, configdict):
		"""
		Kwargs:
			url (str) - The url to an article.
			configdict (str) - A dictionary that contains configurations for different sites
		"""
		self.url = url
		host = urlparse.urlparse(self.url).hostname
		self.config = configdict[host]
		self.soup = self._downloadurl()

	def _downloadurl(self):	
		"""
		Downloads the complete contents of the page at the URL specified in the constructor
		
		Returns:
			soup (BeautifulSoup) - The HTML contents of the page at the URL in a BeautifulSoup class.
		"""
		html = ""	
		response = urllib2.urlopen(self.url)
		html = response.read()
		soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
		return soup

	def gettextlist(self):
		"""
		Extracts a list containing the body text of the article
		
		Returns:
			textlist (list) - The list of words that make out the body text.
		"""
		articlehtml = self.soup.find(self.config["text"]["find"][0], { "class" : re.compile(self.config["text"]["find"][1]) })

		for tag in self.config["text"]["extract"]:
			if(tag[1]):
				[s.extract() for s in self.soup(tag[0], { "class" : tag[1] } )]
			else:
				[s.extract() for s in self.soup(tag[0])]
		
		text = ''.join(articlehtml.findAll(text=True))

		rgx = re.compile("[\w']+", re.UNICODE)
		textlist = rgx.findall(text)
		return textlist

	def getdate(self):
		"""
		Extracts the date of an article, if any is present.
		
		Returns:
			date (datetime) - The date extracted from the article, if it exists
		"""
		logging.info("getdate")
		date = None
		dateelement = self.soup.find(self.config["date"]["find"][0], { "class" : re.compile(self.config["date"]["find"][1]) })
		logging.info(dateelement)
		if dateelement:
			datestring = dateelement.findAll(text=True)[0]
			lf = LocaleFormat()
			date = lf.strptime(datestring, self.config["date"]["format"], "da_DK", "C")
		return date
			
if __name__ == "__main__":
	import sys
	args = sys.argv
	url = args[1]
	configdict = args[2]

	articlescrape = Articlescrape(url, configdict)
	print articlescrape.getdate()
	print articlescrape.gettextlist()
	
	
	