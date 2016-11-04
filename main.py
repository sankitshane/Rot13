import webapp2
import re

form="""
    <form method="post">
        <h2>Enter some text to ROT13:</h2>
        <textarea rows="8" cols="50" name="boxtext">%(text)s</textarea>
        <br>
        <input type="submit">
    </form>
"""

val_form="""
    <form method="post">
        <h2>Signup</h2>
        <div align="right" style="width:300px">
            Username : <input type="text" name="uname">%(unames)s<br />
            Password : <input type="password" name="pass">%(passw)s<br />
            Verify Password : <input type="password" name="v_pass">%(vpassw)s<br />
            Email(optional) : <input type="text" name="email"><br />
        </div>
        <input type="submit">
    </form>
"""

wel_from = """
    <form>
        <h2>Welcome </h2>
    <from>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
on_use = ""
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASS_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)

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

class validate(webapp2.RequestHandler):
    def write_back(self,user="",npass="",vpass=""):
        self.response.out.write(val_form % {"unames":user,"passw":npass,"vpassw":vpass})

    def get(self):
        self.write_back()

    def post(self):
        username = self.request.get('uname')
        password = self.request.get('pass')
        v_password = self.request.get('v_pass')
        email = self.request.get('email')

        pass_uname = valid_username(username)
        pass_password = valid_password(password)
        if email != " ":
            pass_email = True
        else:
            pass_email = valid_email(email)
        if (password == v_password):
            if(pass_uname and pass_password and pass_email):
                self.redirect("/validate/welcome",username)
            else:
                if not pass_uname:
                    self.write_back("NOT Valid","","")
                if not pass_password:
                    self.write_back("","NOT Valid","")
        else:
            self.write_back("","","The passwords are not same")

class welcomeHandler(webapp2.RequestHandler):
    def get(self,username):
        self.response.out.write("Welcome", username)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13',Rot13),
    ('/validate',validate),
    ('/validate/welcome',welcomeHandler)
], debug=True)
