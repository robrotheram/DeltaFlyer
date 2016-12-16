import tornado.web
import tornado


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*");
        self.set_header("Access-Control-Allow-Credentials", "true");
        self.set_header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Key, Authorization");


    def options(self):
        # no body
        self.set_status(204)
        self.finish()
