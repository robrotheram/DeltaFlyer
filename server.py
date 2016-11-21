import io
import tornado.web as web
import tornado.httpserver
import tornado.ioloop
from tornado import concurrent
from concurrent.futures import ThreadPoolExecutor


from routes import route_paths


class App(web.Application):
    def __init__(self):
        web.Application.__init__(self, route_paths)
        self.executor = ThreadPoolExecutor(max_workers=60)


if __name__ == "__main__":
    app = App();
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start()  # autodetect number of cores and fork a process for each
    tornado.ioloop.IOLoop.instance().start()
