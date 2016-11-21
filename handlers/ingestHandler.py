import tornado.web
import json
from kafka import KafkaProducer


class IngestHandler(tornado.web.RequestHandler):
    def get(self):
        producer = KafkaProducer(bootstrap_servers='192.168.1.173:9092')
        r = { "key" : "value" }
        r = json.dumps(r)
        producer.send('test', r)
