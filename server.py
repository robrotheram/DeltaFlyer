import io, os
import tornado.web as web
import tornado.httpserver
import tornado.ioloop
from kafka import KafkaProducer
from tornado import concurrent
from concurrent.futures import ThreadPoolExecutor
from tornado.options import define, options
import logging

from handlers.serverRegisterHandler import *
from handlers.tileHandler import TileHandler
from handlers.userHandler import *
from handlers.ingestHandler import IngestHandler

from handlers.eventsHandler import EventHandler
from handlers.eventsHandler import EventTypeHandler


class App(web.Application):
    def __init__(self):



        #Define config options
        define("port")
        define("address")

        define("token_age")

        #MogoSettings
        define("mongo_host")
        define("mongo_port")
        define("mongo_db")
        define("mongo_user")
        define("mongo_pass")


        #Kafka Settings

        define("kafka_host")
        define("kafka_port")
        define("kafka_topic")

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, "config/config.py")
        options.parse_config_file(path)

        if options.kafka_host is not "":
            kafkaConnection = options.kafka_host+":"+options.kafka_port
            producer = KafkaProducer(bootstrap_servers=kafkaConnection)
        print producer
        self.executor = ThreadPoolExecutor(max_workers=60)

        public_root = os.path.join(os.path.dirname(__file__), 'public')
        configs = {'some_data': 1 }
        route_paths = [
            (r"/(.*)/tile/(.*)/(\d+)/(-?[0-9]+)/(-?[0-9]+)", TileHandler),

            (r'/users/auth', AuthHandler),
            (r'/users/update', UserUpdateHandler),
            (r'/users/register', RegisterHandler),

            (r'/v1/server', ServerHandler),
            (r'/v1/server/regen', ServerAPIKeyRegen),
            (r'/v1/server/list', ServerListHandler),
            (r'/v1/server/update', ServerUpdateHandler),
            (r'/v1/server/register', ServerRegisterHandler),

            #(r'/v1/(.*)/player/(.*)', EventHandler),
            #(r'/v1/(.*)/player/(.*)/stats', EventHandler),

            (r'/v1/(.*)/events/(.*)', EventTypeHandler),
            (r'/v1/(.*)/events', EventHandler),


            (r'/ingest/server', IngestHandler, {'configs' : producer}),
            (r'/(.*)', web.StaticFileHandler, {'path': public_root,"default_filename": "index.html"}),
        ]

        web.Application.__init__(self, route_paths)




if __name__ == "__main__":
    app = App();
    server = tornado.httpserver.HTTPServer(app)

    server.listen(options.port)
    logging.warn("Server istatrting")
    print "Server listening at %s:%s" %(options.address, options.port)
    tornado.ioloop.IOLoop.instance().start()
