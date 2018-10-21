from models import Base, Session
from models import User
# tornado 相关库
from tornado import web
# 做cookie 
import hashlib
import json
from datetime import datetime
import json
import redis 

conn = redis.StrictRedis(host='132.232.72.122',port=6379,db=0)

def LoginRequest(func):
    def check_login(token):
        if conn.hget('login', token) is not None:
            return func()
        else: 
            return 403
    return check_login  

class RegisterHandler(web.RequestHandler):
    def get(self):
        self.render('register.html')
    def post(self):
        md5 = hashlib.md5()
        register_name = self.get_argument('register_name')
        email = self.get_argument('email')
        passwd = self.get_argument('password')
        checking_password = self.get_argument('checking_password')
        
        # request_data = json.loads(body)
        # print(request_data)
        # register_name = request_data.get('register_name')
        # passwd = request_data.get('password')
        # checking_password = request_data.get('checking_password')
        # email = request_data.get('email')
        if passwd != checking_password:
            # 错误处理函数
            pass
        md5.update(passwd.encode('utf-8'))
        hash_password = md5.hexdigest()
        new_user = User(register_name=register_name,passwd=hash_password,email=email)
        session = Session()
        session.add(new_user)
        try:
            session.commit()
            self.write('register successful')
        except:
            session.rollback()
            #抛出异常
            self.write('register failure')

class LoginHandler(web.RequestHandler):
    md5 = hashlib.md5()
    session = Session()
    def get(self):
        self.render('login.html')

    def query_user(self, email):
        return self.session.query(User).filter_by(email=email).first()
    
    # 在redis 中查找令牌,返回一个包含user infomation的dict
    def check_token(self,token):
        user = conn.hget('login', token)
        if user is not None:
            return json.loads(user)
        return None

    # user 是一个包含了user information的dict
    # user = {'id':user.id,'name':user.name,'login_time':datetime.timestamp}
    def set_token(self, token, user):
        user['login_time'] = datetime.timestamp(datetime.now())
        user = json.dumps(user)
        return conn.hset('login', token, user)

    # user 是一个包含了user info的dict
    def update_token(self, token, user):
        user['login_time'] = datetime.timestamp(datetime.now())
        user = json.dumps(user)
        return conn.hset('login',token,user)

    def make_token(self, user):
        return {'id':user.id,
                'login_name':user.name
        }   

    def make_cookie(self,email):
        self.md5.update(email.encode('utf-8'))
        return self.md5.hexdigest()

    def post(self):
        # body = self.request.body
        # login_data = json.loads(body)
        
        # email = login_data.get('email')
        # login_name = login_data.get('login_name')
        # password = login_data.get('password')
        email = self.get_argument('email')
        login_name = self.get_argument('login_name')
        password = self.get_argument('password')
        if login_name is None or password is None or email is None:
            self.set_status(403)
            self.write({'message':'data missing'})
        self.md5.update(password.encode('utf-8'))
        hash_passwd = self.md5.hexdigest()
        
        # 先从缓存中寻找，如果不存在在从数据库中查找
        login_user = self.check_token(email)
        if login_user is not None:
            self.update_token(email,login_user)
            self.set_status(403)
            self.write({'message':'had login'})
            return 
        login_user = self.query_user(email)
        print(login_user)
        if login_user is None:
            self.set_status(404)
            self.write({'message':'no user'}) 
            return 
        elif login_user.hashed_passwd == hash_passwd:
            self.set_cookie('email',self.make_cookie(email))
            self.set_token(login_user.email,self.make_token(login_user))
            return self.write({'message':'login successful'})
        return self.write({'message':'password wrong'})