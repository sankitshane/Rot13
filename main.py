import webapp2

form="""
    <form method="post">
        <h2>Enter some text to ROT13:</h2>
        <textarea rows="8" cols="50" name="boxtext">%(text)s</textarea>
        <br>
        <input type="submit">
    </form>
"""

class MainPage(webapp2.RequestHandler):
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

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
