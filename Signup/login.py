import webapp2
import os
import jinja2
import re

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape= True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)

class Signup(Handler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            new = User(username = username, password = password)
            new.put()
            self.response.headers.add_header('Set-Cookie','user = %s' % str(username))
            self.redirect('/welcome')

class login(Handler):
    def get(self):
        self.render('login.html')
    def post(self):
        username = self.request.get('login_name')
        password = self.request.get('pass')

        if username and password:
            validate = db.GqlQuery("SELECT * FROM User WHERE username= :1 and password= :2",str(username),str(password))
            if validate:
                self.response.headers.add_header('Set-Cookie','user = %s'% str(username))
                self.redirect('/welcome')
            else:
                self.redirect('/login')
        else:
            self.redirect('/login')

class logout(webapp2.RequestHandler):
    def get(self):
        a = " "
        self.response.headers.add_header('Set-Cookie','user=; Path=/')
        self.redirect('/signup')
