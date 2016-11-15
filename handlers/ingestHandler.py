import tornado.web
import json
from kafka import KafkaProducer


class IngestHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        producer = KafkaProducer(bootstrap_servers='192.168.1.173:9092')
        r = json.dumps(data)
        producer.send('test', r).get(timeout=60)
        response = { 'message': 'Welcome to the coolest API on earth to kafka send!' }
        self.write(response)
