import io, os
import tornado.web as web
import tornado.httpserver
import tornado.ioloop
from tornado import concurrent
from concurrent.futures import ThreadPoolExecutor
from tornado.options import define, options
import logging

from routes.routes import route_paths


class App(web.Application):
    def __init__(self):
        web.Application.__init__(self, route_paths)
        self.executor = ThreadPoolExecutor(max_workers=60)

        #Define config options
        define("port")

        #MogoSettings
        define("mongo_host")
        define("mongo_port")
        define("mongo_user")
        define("mongo_pass")


        #Kafka Settings

        define("kafka_host")
        define("kafka_port")
        define("kafka_topic")


        dir = os.path.dirname(__file__)
        path = os.path.join(dir, "config/config.py")
        tornado.options.parse_config_file(path)




if __name__ == "__main__":
    app = App();
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    logging.warn("Server istatrting")
    print options.as_dict()
    tornado.ioloop.IOLoop.instance().start()
