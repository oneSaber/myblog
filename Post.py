from models import Post, Comment, User
from models import Session
from tornado import web
from User import conn
import json
import os
import markdown

class UploadHandler(web.RequestHandler):
    
    # 如果存在cooike 为email,
    # redis中有相关数据则返回poster为string` {'id':user.id,'name':user.name,'login_time':datetime.timestamp}`
    # 如果不存在则返回None
    def checking_Login(self):
        email = self.get_cookie('email')
        print("cookie: "+email)
        if email is not None:
            poster = conn.hget('login',email)
            return poster
        else:
            return None

    # return User or None  
    def query_poster(self, poster_id):
        session = Session()
        return session.query(User).filter_by(id=poster_id).first()

    def get(self):
        self.render("post.html")

    def checking_user(self):
        cache = self.checking_Login()
        if cache is None:
            self.set_status(403)
            return self.write({'msg':'must login'})
        user_info = json.loads(cache)
        poster = self.query_poster(user_info['id'])
        if poster is None:
            self.set_status(404)
            return  self.write({'msg':"can't find the user"})
        else:
             return poster     
    def postFile(self):
        upload_path = os.path.join(os.path.dirname(__file__),'files')
        file_mates = self.request.files.get('file', None) # 提取表单中的file元素
        print(len(file_mates))
        if file_mates is None:
            self.set_status(403)
            return self.write({'msg':'no file'})
        for mate in file_mates:
            file_name = mate['filename']
            file_path = os.path.join(upload_path,file_name)
            with open(file_path,"wb") as up:
                up.write(mate['body'])
        self.write('upload successful')
    
    def post(self):
        poster = self.checking_user()
        if self.request.files.get('file',None) is not None:
            return self.postFile()
        else:
            title = self.get_argument('title')
            entry = self.get_argument('entry')
            # use markdown change post
            new_post = Post(title=title,author_id=poster.id,markdown=entry)
            session = Session()
            session.add(new_post)
            session.commit()