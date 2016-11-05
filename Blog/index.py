import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape= True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class blog(Handler):
    def get(self):
        self.render("blog.html")

class newpost(Handler):
    def render_newpost(self,title="",content="",error=""):
        self.render("newpost.html",title=title,content=content,error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')

        if title and content:
            self.redirect('/blog')
        else:
            error = "we need both the subject and content"
            self.render_newpost(title,content,error)
#app = webapp2.WSGIApplication([('/',MainPage)],debug=True)
