
from handlers.serverHandler import ServerHandler
from handlers.tileHandler import TileHandler
from handlers.userHandler import AuthHandler

import tornado.web as web
import os
public_root = os.path.join(os.path.dirname(__file__), 'public')
route_paths = [
    #(r"/", MainHandler),
    (r"/img/(\d+)/(-?[0-9]+)/(-?[0-9]+)", TileHandler),
    (r'/(.*)', web.StaticFileHandler, {'path': public_root,"default_filename": "index.html"}),
    (r'/users/auth', AuthHandler),
    (r'/users/register', ServerHandler),
    (r'/server', ServerHandler),
    (r'/server/register', ServerHandler),
    (r'/player/(.*)', ServerHandler),
    (r'/events/(.*)', ServerHandler),
    (r'/ingest', ServerHandler),
]
