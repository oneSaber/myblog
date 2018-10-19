from models import Base, Session
from models import User
from blog import conn
# tornado 相关库
from tornado import web
# 做cookie 
import hashlib
import json
from datetime import time

class Register(web.RequestHandler):
    def get(self):
        self.render('register.html')
    def post(self):
        md5 = hashlib.md5()
        register_name = self.get_argument('register_name')
        email = self.get_argument('email')
        passwd = self.get_argument('password')
        checking_password = self.get_argument('checking_password')
        if passwd != checking_password:
            # 错误处理函数
        md5.update(passwd.encode('utf-8'))
        hash_password = md5.hexdigest()
        new_user = User(register_name=register_name,passwd=hash_password)
        session = Session()
        session.add(new_user)
        try:
            session.commit()
            self.render('index.html')
        except:
            session.rollback()
            #抛出异常
            self.render('register.html')

class Login(web.RequestHandler):
    self.md5 = hashlib.md5()
    self.session = Session()
    def get(self):
        self.render('login.html')

    def query_user(self, login_name):
        return self.session.query(User).filter_by(name=login_name).first()
    
    # 在redis 中查找令牌
    def check_token(self,token):
        return conn.hget('login', token)

    def set_token(self, token, user):
        return conn.hset('login', token, user)

    def update_token(self, token, session):
        timestamp = time.time()



    def psot(self):
        login_name = self.get_argument('login name')
        password = self.get_argument('password')
        self.md5.update(password.encode('utf-8'))
        hash_passwd = self.md5.hexdigest()
        # 先从缓存中寻找，如果不存在在从数据库中查找
        login_user = self.check_token(login_name)
        