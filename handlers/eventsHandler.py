import tornado.web
from auth.jwtauth import jwtauth
from database.Events import EventDocuments

@jwtauth
class EventTypeHandler(tornado.web.RequestHandler):
    def get(self,servername,type):
        try:
            time = int(self.get_argument("time", default=None, strip=False))
            delta = int(self.get_argument("delta", default=None, strip=False))
            list = (self.get_argument("filter", default=None, strip=False))
            if list is not None:
                list = list.split(',')

        except TypeError, e:
            time = 0
            delta = 60
        collection = servername+"_events"
        ed = EventDocuments().getEvents(collection,time,delta).filter("EventType",[type]).execute()


        if list is not None:
            ed.refine(list)

        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.write(ed.toJson())

@jwtauth
class EventHandler(tornado.web.RequestHandler):
    def get(self,servername):

        try:
            time = int(self.get_argument("time", default=None, strip=False))
            delta = int(self.get_argument("delta", default=None, strip=False))
            list = (self.get_argument("filter", default=None, strip=False))
            if list is not None:
                list = list.split(',')

        except TypeError, e:
            time = 0
            delta = 60
        collection = servername+"_events"
        ed = EventDocuments().getEvents(collection,time,delta).execute()
        if list is not None:
            ed.refine(list)

        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.write(ed.toJson())
