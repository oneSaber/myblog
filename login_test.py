import requests
from datetime import datetime
se = requests.Session()

def register():
    data = {'register_name':'faker','email':'12567@qq.com','password':'12345qwert','checking_password':'12345qwert'}
    re = se.post(url='http://localhost:5000/register',data=data)
    print(re)

def login():
    data = {'email':'233@qq.com','password':'12345qwert','login_name':'faker'}
    begin_time = datetime.now()
    re = se.post(url='http://localhost:5000/login',data=data)
    print(re.content)
    end_time = datetime.now()
    print((end_time-begin_time).seconds)

if __name__ == '__main__':
    # register()
    login()