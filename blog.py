# 每次添加了新的api都需要重启服务
import os
from tornado import ioloop, web, httpserver
from tornado import options
from models import Base
from tornado.options import define

define('port',default=5000, help='web port', type=int)
define('debug',default=True, help='debug model', type=bool)

# 处理器列表
handler = []
class EntryModule(web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)

class Application(web.Application):
    def __init__(self):
        handlers = handler
        settings = dict(
            blog_title=u"sample-bbs",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True
        )
        super(Application,self).__init__(handlers,**settings)
