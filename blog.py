# 每次添加了新的api都需要重启服务
import os
from tornado import ioloop, web, httpserver
from tornado import options
from models import Base,engine
from Handler import IndexHandler
from User import RegisterHandler,LoginHandler
from Post import UploadHandler

from tornado.options import define, options
define('port',default=5000, help='web port', type=int)
define('debug',default=True, help='debug model', type=bool)


class EntryModule(web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)

class Application(web.Application):
    def __init__(self, db):    
        self.db = db
        handlers =[
            (r'/', IndexHandler),
            (r'/register', RegisterHandler),
            (r'/login', LoginHandler),
            (r'/uploadentry',UploadHandler)
        ] 
        settings = dict(
            blog_title=u"sample-bbs",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule},
            # xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True
        )
        super(Application,self).__init__(handlers,**settings)

if __name__ == '__main__':
    # 一直呼叫直到redis 应答
    app = Application(db=engine)
    app.listen(port=options.port)
    server = httpserver.HTTPServer(app)
    ioloop.IOLoop.instance().start()