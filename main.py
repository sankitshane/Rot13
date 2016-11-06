import webapp2
import re
from Blog.index import blog,newpost,Postpage
from Signup.login import Signup

form="""
    <form method="post">
        <h2>Enter some text to ROT13:</h2>
        <textarea rows="8" cols="50" name="boxtext">%(text)s</textarea>
        <br>
        <input type="submit">
    </form>
"""

wel_from = """
    <form>
        <h2>Welcome </h2>
    <from>
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

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to my app")



class welcomeHandler(webapp2.RequestHandler):
    def get(self):
        user = self.request.cookies.get('user')
        a = 'welcome ' + user
        self.response.out.write(a)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13',Rot13),
    ('/signup',Signup),
    ('/welcome',welcomeHandler),
    ('/blog',blog),
    ('/blog/newpost',newpost),
    ('/blog/([0-9]+)',Postpage)
], debug=True)
