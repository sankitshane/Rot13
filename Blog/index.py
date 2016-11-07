import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape= True)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

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
        if self.user:
            self.render_newpost()
        else:
            self.redirect('/login')

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content').replace('\n', '<br>')

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
