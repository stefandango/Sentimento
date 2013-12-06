#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:mod:`mainpage` -- Used for serving the web interface to the users
==================================================================

:synopsis: Produces the webpages, using jinja2, and handles API calls.

Requirements::
	1.	The webapp2 framwework
		http://webapp-improved.appspot.com/
	2.	The jinja2 framework
		http://jinja.pocoo.org/
    3.  The Google App Engine launcher is used to launch the application
		https://developers.google.com/appengine/
"""

import webapp2
import jinja2
import json
import os
import time
import mainmodule
import config

__version__ = 1.00
__author__ = "Group 21"
__all__ = ["mainpage"]

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		"""
		Creates the main page, using a Jinja template.
		"""
		template_values = {"site_list": config.MEDIALIST}
		template = JINJA_ENVIRONMENT.get_template('scrape.html')
		self.response.write(template.render(template_values))

class ShowResults(webapp2.RequestHandler):
	"""
	Creates the results page, using a Jinja template.
	"""
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render({}))
		
class Api(webapp2.RequestHandler):
	"""
	Performs a call to the module, to perform the Sentiment analysis, using paramters defined in the URL
	"""
	def get(self):
		topic = self.request.get('Topic')
		Sources = self.request.get('Sources').split(",")

		media = []
		for s in Sources:
			if(s in config.MEDIADICT.keys()):
				media.append(config.MEDIADICT[s])

		startdate = self.request.get('Startdate')
		enddate = self.request.get('Enddate')

		if(startdate != "" or enddate != ""):
			startdate = time.strptime(self.request.get('Startdate'), "%d-%m-%Y")
			enddate = time.strptime(self.request.get('Enddate'), "%d-%m-%Y")
		
		if(startdate != "" and enddate != ""): 	
			analysismodule = mainmodule.sentimentanalysismodule(media, topic, startdate, enddate)
		else:
			analysismodule = mainmodule.sentimentanalysismodule(media, topic)

		data = analysismodule.startanalysis()
		self.response.write(json.dumps(data))

#Handled by Google App Engine Launcher
application = webapp2.WSGIApplication([
	('/', MainPage),
    ('/result', ShowResults),
	('/api', Api),
], debug=True)

