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
        blogs = db.GqlQuery("SELECT * FROM new_blog ORDER BY created DESC")
        self.render("blog.html",blogs= blogs)

class new_blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class newpost(Handler):
    def render_newpost(self,title="",content="",error=""):
        self.render("newpost.html",title=title,content=content,error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')

        if title and content:
            one = new_blog(title= title,content = content)
            one.put()
            self.redirect('/blog/%s' % str(one.key().id()))
        else:
            error = "we need both the subject and content"
            self.render_newpost(title,content,error)

class Postpage(Handler):
    def get(self,post_id):
        key = db.Key.from_path('new_blog',int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return
        self.render("permalink.html", post=post)
#app = webapp2.WSGIApplication([('/',MainPage)],debug=True)
