# myapp.py
import os

import tornado.ioloop
import tornado.web
import tornado.template
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html") 

class LoginUser(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")

    def post(self):
        #login
        pass

class LogoutUser(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class RegisterUser(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html") 

    def post():
        pass

class StartNethack(tornado.web.RequestHandler):
    def get(self):
        self.render("interface.html")



def main():
    return tornado.web.Application([
        (r"/", Index),
        (r"/login", LoginUser),
        (r"/logout", LogoutUser),
        (r"/register", RegisterUser),
        (r"/start", StartNethack),
        ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=options.debug,
    )

if __name__ == "__main__":
    app = main()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


