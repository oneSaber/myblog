from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Table
from sqlalchemy import String, Integer, Text, TIME
from sqlalchemy import ForeignKey
from datetime import datetime
import redis 

conn = redis.StrictRedis(host='132.232.72.122',port=6379,db=0)

# engine = create_engine("sqlite:///blog.db", echo=True)
# engine = create_engine("mysql+pymysql://root:123456@132.232.72.122:3306/blog", echo=True)
engine = create_engine("mysql+pymysql://zsj:123456@39.105.64.7:3306/blog",echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, nullable=False)
    hashed_passwd = Column(String(64), nullable=False)
    email = Column(String(64), nullable=True)
    slogn = Column(String(64)) # 个人签名
    avatar = Column(String(64)) # 头像连接

    def __init__(self, register_name, passwd, email, **kwargs):
        self.name = register_name
        self.hashed_passwd = passwd
        self.email = email
        self.slogn = kwargs.get('slogn', None)
        self.avatar = kwargs.get('avatar', None)
    
    def __repr__(self):
        return '<User({id},{name},{slogn},{avatar})>'.format(
            id=self.id, name=self.name, slogn=self.slogn, avatar=self.avatar)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True, nullable=False)
    markdown = Column(Text, nullable=False)
    # html = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(TIME)

    user = relationship("User", backref='posts')
    
    def __init__(self, title, author_id, markdown):
        self.title = title
        self.author_id = author_id,
        # self.html = html
        self.markdown = markdown
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return '<Post({id},{title},{author_id},{time})>'.format(
            id= self.id,title=self.title,author_id=self.author_id,
            time=self.timestamp)
        

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    # 主贴id
    post_id = Column(Integer,ForeignKey('posts.id'))
    # 发帖人id
    author_id = Column(Integer, ForeignKey('users.id'))
    html = Column(Text)
    markdown = Column(Text)
    timestamp = Column(TIME)

    main_post = relationship('Post',backref='comments')
    author = relationship('User',backref='comments')

    def __init__(self, post_id,author_id,html,markdown):
        self.author_id = author_id
        self.post_id = post_id
        self.html = html
        self.markdown = markdown
        self.timestamp = datetime.now()

if __name__ == '__main__':
    Base.metadata.create_all()
    session = Session()
    frist_user = User(register_name='saber',passwd='123456',slogn='hello world',email='123@qq.com')
    session.add(frist_user)
    session.commit()