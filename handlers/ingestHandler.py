import tornado.web
import json

from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer
from tornado.options import options
from tornado.concurrent import run_on_executor
from handlers.auth.serverjwtauth import serverjwtauth


@serverjwtauth
class IngestHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=100)



    @run_on_executor
    def background_task(self, data, serverName, producer):
        """ This will be executed in `executor` pool. """

        try:
            data["meta"] = {"serverID":serverName};
            r = json.dumps(data)
            producer.send(options.kafka_topic, r).get(timeout=1)
            return True
        except Exception,e:
            print e
            return False


    def initialize(self, configs):
        self.producer = configs;


    @tornado.gen.coroutine
    def post(self):
        serverName = self.request.headers.get("serverName")
        res = yield self.background_task(tornado.escape.json_decode(self.request.body), serverName,self.producer)
        if res:
            response = { 'message': 'Event Submitted',"serverID":serverName}
        else:
            response = {'message': 'Broker',"serverID":serverName}
        self.write(response)
