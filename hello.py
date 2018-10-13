from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado import web
import textwrap

from tornado.options import define,options
define('port',default=5000,help='run on the given port',type=int)

class RevserHandler(web.RequestHandler):
    def get(self,input):
        self.write(input[::-1])

class WrapHandler(web.RequestHandler):
    def get(self):
        text = self.get_argument('text')
        width = self.get_argument('width',40)
        self.write(textwrap.fill(text,int(width)))

class IndexHandler(web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting','hello')
        self.write(greeting + ' firendly user!')

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        [
            (r"/",IndexHandler),
            (r"/revser/(\w+)",RevserHandler),
            (r"/wrap",WrapHandler),
        ]
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()