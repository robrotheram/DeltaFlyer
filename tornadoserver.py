import io
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import concurrent
from tornado import gen
import tornado.web as web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
import math
import os
from Tile import Tile

public_root = os.path.join(os.path.dirname(__file__), 'public')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world %s" % time.time())

class SleepHandler(tornado.web.RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(8)

    tile_size = 256
    world_size = 6000 #number of blocks
    pixel_size = (world_size/16)*tile_size # number of pixels based on 1 chunk = 256
    max_zoom = math.ceil((np.log((pixel_size/tile_size)) / np.log(2)))
    map_max_size = math.pow(2,max_zoom)*tile_size


    def is_tile_invalid(self,zoom,x,y):
        #print(self.max_zoom)
        bounds = math.pow(2,(self.max_zoom-zoom))*256
        xb = bounds+(bounds*x)
        yb = bounds+(bounds*y)
        #print(xb)
        if(xb > self.map_max_size or xb <= 0 or yb > self.map_max_size or yb <= 0):
            return True
        else:
            return False


    @tornado.gen.coroutine
    def get(self, z,x,y):
        print((z,x,y))
        # if (self.is_tile_invalid(int(z),int(x),int(y))):
        #     self.write("NOT VALID")
        #     self.finish()
        #     return

        n = yield self._exe(z,x,y)
        self.set_header('Content-Type', 'image/jpg')
        self.write(n)
        self.finish()

    @run_on_executor
    def _exe(self,z,x,y):
        tile = Tile()
        image = tile.rendertile(int(z),int(x),int(y))
        imgbuff = io.BytesIO()
        image.save(imgbuff,format="jpeg")
        return imgbuff.getvalue()


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            #(r"/", MainHandler),
            (r"/img/(\d+)/(-?[0-9]+)/(-?[0-9]+)", SleepHandler),
            (r'/(.*)', web.StaticFileHandler, {'path': public_root,"default_filename": "index.html"}),
        ]
        tornado.web.Application.__init__(self, handlers)
        self.executor = ThreadPoolExecutor(max_workers=60)


if __name__ == "__main__":
    app = App();
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start()  # autodetect number of cores and fork a process for each
    tornado.ioloop.IOLoop.instance().start()
