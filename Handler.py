from tornado import web
from models import User, Post, Comment
from models import Base,Session

class IndexHandler(web.RequestHandler):
    def get(self):
        session = Session()
        # 按时间顺序的前10
        all_artices = session.query(Post).order_by(Post.timestamp)[:10]
        if len(all_artices) == 0:
            # self.redirect('/compose')
           self.write('index.html')
        return self.render('home.html',artices=all_artices)
