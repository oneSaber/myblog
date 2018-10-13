import os.path

from tornado import web
from tornado import ioloop
from tornado import httpserver
from tornado import options

from tornado.options import define,options
define('port',default=5000,help='run on the given port',type=int)

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemHandler(web.RequestHandler):
    def post(self):
        non1 = self.get_argument('noun1')
        non2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        non3 = self.get_argument('noun3')
        self.render('poem.html',roads = non1,wood = non2,
        made = verb,difference = non3)

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[
            (r'/index',IndexHandler),
            (r'/poem',PoemHandler)
        ],
        template_path =os.path.join(os.path.dirname(__file__),'templates')
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()