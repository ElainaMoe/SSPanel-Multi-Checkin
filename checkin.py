import requests
import os
import time
import json
requests.packages.urllib3.disable_warnings()

if os.path.exists('site') and os.path.exists('users') and os.path.exists('pwd'):
    print('检测到当前目录下存在配置文件，正在读取……')
    site_file, user_file, pwd_file = open('site'), open('users'), open('pwd')
    base_url = site_file.read()
    user_list = user_file.read()
    pwd_list = pwd_file.read()
    site_file.close()
    user_file.close()
    pwd_file.close()
    if(base_url == "" or user_list == "" or pwd_list == ""):
        print("配置文件未填写完全，请重试！")
        exit()
else:
    base_url = os.environ["websites"]
    user_list = os.environ["user_list"]
    pwd_list = os.environ["pwd_list"]
    if(base_url == "" or user_list == "" or pwd_list == ""):
        print("发生异常，一个或多个环境变量无法读取，请检查您Fork的仓库的secret设定")
        exit()


# 分割账号密码开头
website = base_url.split('\n')
user = user_list.split("\n")
pwd = pwd_list.split("\n")
# 分割账号密码结尾


def checkin(url, email, password):
    print(f'正在对 {url} 进行连接测试……')
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError as e:
        print(f'对 {url} 的链接测试失败，请检查该链接是否可以正常访问：{e}')
        return
    print(f'开始对 {url} 进行签到……')
    email = email.split('@')
    email = email[0] + '%40' + email[1]

    session = requests.session()

    res = session.get(url, verify=False)
    # print(res.text)
    time.sleep(10)  # 防止某些站带有DDOS保护验证
    res = session.get(url, verify=False)
    # print(res.text)
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
    if response.status_code == 200:
        try:
            print(json.loads(response.text)['msg']])
        except Exception as e:
            print(f'[ERROR] Critical error when parsing, {e}')
            print(str(response.text))
    elif response.status_code >= 400 and response.status_code < 500:
        print(f'签到发生错误，返回状态码为 {response.status_code} ，返回体为{response.text}')
    elif response.status_code > 500:
        print(f'签到发生错误，返回状态码为 {response.status_code} ，貌似机场出了点问题？返回体为{response.text}')


datas = []
for i in range(min(len(website), len(user), len(pwd))):
    datas.append((website[i], user[i], pwd[i]))

for data in datas:
    url, user, pwd = data
    checkin(url, user, pwd)
