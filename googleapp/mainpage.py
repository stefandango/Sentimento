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
import cgi
import logging
import time
import mainmodule

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

mediadict = {"INF": "information.dk", "TV2": "nyhederne.tv2.dk", 
		"POL": "politiken.dk", "EB": "ekstrabladet.dk", "BT": "bt.dk"}

medialist = [{"id": "INF", "display": "information.dk" }, 
		{"id": "TV2", "display": "nyhederne.tv2.dk" }, 
		{"id": "POL", "display": "politiken.dk" }, 
		{"id": "EB", "display": "ekstrabladet.dk" }, 
		{"id": "BT", "display": "bt.dk" }]

test_data = [['Score', 'Ekstrabladet.dk', 'BT.dk', 'Information.dk', 'nyhderne.tv2.dk'],
		['Lars Loekke Rasmussen',  3.5, 4.5, 5.9, -3.3]]



class MainPage(webapp2.RequestHandler):
    def get(self):
	"""
	Creates the main page, using a Jinja template.
	"""
		template_values = {"site_list": medialist}
		template = JINJA_ENVIRONMENT.get_template('scrape.html')
		self.response.write(template.render(template_values))

class ShowResults(webapp2.RequestHandler):
	"""
	Creates the results page, using a Jinja template.
	"""
	def get(self):
		calc = ((len(test_data) - 1) * 400) + 100
		width = min(calc, 1200)
		template_values = {"sentimento_data": test_data, "chart_width": width}
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render(template_values))
		
class Api(webapp2.RequestHandler):
	"""
	Performs a call to the module, to perform the Sentiment analysis, using paramters defined in the URL
	"""
	def get(self):
		topic = self.request.get('Topic')
		Sources = self.request.get('Sources').split(",")

		media = []
		for s in Sources:
			if(s in mediadict.keys()):
				media.append(mediadict[s])

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

