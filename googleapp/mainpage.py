import webapp2
import jinja2
import os
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

medialist = [{"id": "INF", "display": "information.dk" }, 
		{"id": "TV2", "display": "nyhederne.tv2.dk" }, 
		{"id": "POL", "display": "politiken.dk" }, 
		{"id": "EB", "display": "ekstrabladet.dk" }, 
		{"id": "BT", "display": "bt.dk" },]



class MainPage(webapp2.RequestHandler):

    def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('scrape.html')
		self.response.write(template.render(template_values))

class ShowResults(webapp2.RequestHandler):

	def get(self):

		for medium in medialist:
			if(self.request.get(medium["id"])):
				pass #get what media to add to search list medium.display

		topic = (cgi.escape(self.request.get('Topic')))

		template_values = {"Topic": topic}
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/result', ShowResults),
], debug=True)

