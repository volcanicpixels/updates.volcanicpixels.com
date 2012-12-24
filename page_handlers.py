import webapp2

class NotFoundPage(webapp2.RequestHandler):
	def get(self):
		self.error(404)
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(open('static_pages/not_found.html').read())

class ApiErrorPage(webapp2.RequestHandler):
	def get(self):
		self.error(404)
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(open('static_pages/api_error.html').read())

class LandingPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(open('static_pages/landing.html').read())

app = webapp2.WSGIApplication([('/api/.*', ApiErrorPage),('/', LandingPage),('/.*', NotFoundPage)],
							  debug=True)