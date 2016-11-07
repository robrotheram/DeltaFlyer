import io


import tornado.ioloop
import tornado.web


from Tile import Tile

import time

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor   # `pip install futures` for python2

MAX_WORKERS = 4


class Handler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor
    def background_task(self, i):
        """ This will be executed in `executor` pool. """
        time.sleep(10)
        return i

    @tornado.gen.coroutine
    def get(self):
        """ Request that asynchronously calls background task. """
        res = yield self.background_task('300')
        self.write(res)

class Foo(tornado.web.RequestHandler):
    def get(self):
        self.write('foo')

class Bar(tornado.web.RequestHandler):
    def get(self):
        tile = Tile()
        image = tile.get4chunks()
        imgbuff = io.BytesIO()
        image.save(imgbuff,format="jpeg")
        self.set_header('Content-Type', 'image/jpg')
        self.write(imgbuff.getvalue())

class SimonSays(tornado.web.RequestHandler):
    def get(self):
        say = self.get_argument("say")
        self.write('Simon says, %s' %say)

def make_app():
    return tornado.web.Application([
        (r"/long", Handler),
        (r"/foo", Foo),
        (r"/bar", Bar),
        (r"/simonsays", SimonSays),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


