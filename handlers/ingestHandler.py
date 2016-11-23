import tornado.web
import json

from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer
from tornado.concurrent import run_on_executor


class IngestHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=100)
    producer = KafkaProducer(bootstrap_servers='192.168.1.173:9092')

    @run_on_executor
    def background_task(self, data):
        """ This will be executed in `executor` pool. """
        data["meta"] = {"serverID":"testACCOUNT"};
        r = json.dumps(data)
        self.producer.send('test', r).get(timeout=1)
        return True

    @tornado.gen.coroutine
    def post(self):
        """ Request that asynchronously calls background task. """
        res = yield self.background_task(tornado.escape.json_decode(self.request.body))
        response = { 'message': 'Welcome to the coolest API on earth to kafka send!' }
        self.write(response)

