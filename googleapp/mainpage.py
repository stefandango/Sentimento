import webapp2
import jinja2
import json
import os
import cgi
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

medialist = [{"id": "INF", "display": "information.dk" }, 
		{"id": "TV2", "display": "nyhederne.tv2.dk" }, 
		{"id": "POL", "display": "politiken.dk" }, 
		{"id": "EB", "display": "ekstrabladet.dk" }, 
		{"id": "BT", "display": "bt.dk" }]

test_data = [['Score', 'Ekstrabladet.dk', 'BT.dk', 'Information.dk', 'nyhderne.tv2.dk'],
		['Lars Loekke Rasmussen',  3.5, 4.5, 5.9, -3.3]]

class MainPage(webapp2.RequestHandler):
    def get(self):
		template_values = {"site_list": medialist}
		template = JINJA_ENVIRONMENT.get_template('scrape.html')
		self.response.write(template.render(template_values))

class ShowResults(webapp2.RequestHandler):
	def get(self):
		calc = ((len(test_data) - 1) * 400) + 100
		width = min(calc, 1200)
		template_values = {"sentimento_data": test_data, "chart_width": width}
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render(template_values))
		
class Api(webapp2.RequestHandler):
	def get(self):

		#Sanitize input 
		Topic = self.request.get('Topic')
		Sources = self.request.get('Sources').split(",")

		

		jsonObj = json.dumps(test_data)
		self.response.write(jsonObj)
		logging.info('-----------test variable: %s', Sources)
application = webapp2.WSGIApplication([
	('/', MainPage),
    ('/result', ShowResults),
	('/api', Api),
], debug=True)

