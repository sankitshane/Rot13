import webapp2
import re
import os
import jinja2

from Blog.index import blog,newpost,Postpage
from Signup.login import Signup,login,logout

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape= True)

form="""
    <form method="post">
        <h2>Enter some text to ROT13:</h2>
        <textarea rows="8" cols="50" name="boxtext">%(text)s</textarea>
        <br>
        <input type="submit">
    </form>
"""

class Rot13(webapp2.RequestHandler):
    def rot13(self,n_text):
        res = ""
        for c in n_text:
            if c.isalpha():
                if c.isupper():
                    num = ord(c)
                    if num + 13 < 91:
                        res += chr(num + 13)
                    else:
                        res += chr(64 + ((num+13)-90))
                else:
                    num = ord(c)
                    if num + 13 < 123:
                        res += chr(num + 13)
                    else:
                        res += chr(96 +((num + 13)-122))
            else:
                res += c
        return res
    def write_back(self,text=""):
        self.response.out.write(form % {"text":text})

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write(form)
        self.write_back()
    def post(self):
        text = self.request.get("boxtext")
        self.write_back(self.rot13(text))

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class welcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = self.request.cookies.get('user')
        if user:
            a = 'welcome ' + user
            self.response.out.write(a)
        else:
            self.redirect('/signup')

class MainPage(Handler):
    def get(self):
        self.render("welcome.html")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13',Rot13),
    ('/signup',Signup),
    ('/welcome',welcomeHandler),
    ('/blog',blog),
    ('/blog/newpost',newpost),
    ('/blog/([0-9]+)',Postpage),
    ('/login',login),
    ('/welcome/logout',logout)
], debug=True)
