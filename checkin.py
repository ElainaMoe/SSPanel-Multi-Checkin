import requests
import os
import time
requests.packages.urllib3.disable_warnings()


# 初始化环境变量开头
base_url = os.environ["websites"]
user_list = os.environ["user_list"]
pswd_list = os.environ["pwd_list"]
# 初始化环境变量结尾

if(base_url == "" or user_list == "" or pswd_list == ""):
    print("发生异常，一个或多个环境变量无法读取，请检查您Fork的仓库的secret设定")
    exit()


# 分割账号密码开头
website = base_url.split('\n')
user = user_list.split("\n")
pwd = pswd_list.split("\n")
# 分割账号密码结尾


def checkin(url, email, password):

    email = email.split('@')
    email = email[0] + '%40' + email[1]

    session = requests.session()

    session.get(url, verify=False)
    time.sleep(10)  # 防止某些站带有DDOS保护验证
    session.get(url, verify=False)
    login_url = url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data,
                            headers=headers, verify=False)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': url + '/user'
    }

    response = session.post(url + '/user/checkin',
                            headers=headers, verify=False)
    print(response.text)


datas = []
for i in range(min(len(website), len(user), len(pwd))):
    datas.append((website[i], user[i], pwd[i]))

for data in datas:
    url, user, pwd = data
    checkin(url, user, pwd)