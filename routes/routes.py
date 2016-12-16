
from handlers.serverRegisterHandler import ServerRegisterHandler, ServerHandler, ServerListHandler
from handlers.tileHandler import TileHandler
from handlers.userHandler import AuthHandler
from handlers.userHandler import RegisterHandler
from handlers.ingestHandler import IngestHandler

from handlers.eventsHandler import EventHandler
from handlers.eventsHandler import EventTypeHandler

import tornado.web as web
import os
public_root = os.path.join(os.path.dirname(__file__), '../public')
route_paths = [
    (r"/(.*)/tile/(.*)/(\d+)/(-?[0-9]+)/(-?[0-9]+)", TileHandler),

    (r'/users/auth', AuthHandler),
    (r'/users/register', RegisterHandler),

    (r'/v1/server', ServerHandler),
    (r'/v1/server/list', ServerListHandler),
    (r'/v1/server/register', ServerRegisterHandler),

    #(r'/v1/(.*)/player/(.*)', EventHandler),
    #(r'/v1/(.*)/player/(.*)/stats', EventHandler),

    (r'/v1/(.*)/events/(.*)', EventTypeHandler),
    (r'/v1/(.*)/events', EventHandler),


    (r'/ingest/server', IngestHandler),
    (r'/(.*)', web.StaticFileHandler, {'path': public_root,"default_filename": "index.html"}),
]
