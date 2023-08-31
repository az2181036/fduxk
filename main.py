import time
import execjs
import requests

from bs4 import BeautifulSoup


def get_query_vcode_img(timestamp):
    query_vcode = requests.get(token_url + timestamp)
    query_vcode_token = query_vcode.json()['data']['token']
    vcode_img = requests.get(img_url + query_vcode_token)

    with open('vcode_img.png', "wb") as f:
        f.write(vcode_img.content)

    return query_vcode_token


# 设置登录页面的URL
base_url = 'http://yjsxk.fudan.edu.cn/yjsxkapp'
index_url = base_url + '/sys/xsxkappfudan/*default/index.do'
login_url = base_url + '/sys/xsxkappfudan/login/check/login.do?timestrap='
token_url = base_url + "/sys/xsxkappfudan/login/4/vcode.do?timestamp="
img_url = base_url + '/sys/xsxkappfudan/login/vcode/image.do?vtoken='
course_url = base_url + "/sys/xsxkappfudan/xsxkHome/gotoChooseCourse.do"
choice_course_url = base_url + "/sys/xsxkappfudan/xsxkCourse/choiceCourse.do?_="

# 创建一个会话
session = requests.Session()

with open('js.js', 'r') as f:
    js_code = f.read()
    js = execjs.compile(js_code)
timestamp = str(execjs.eval("(new Date).getTime()"))
while True:
    token = get_query_vcode_img(timestamp=timestamp)
    print("请查看文件目录下的vcode_img.png，输入验证码：")
    captcha_rst = input()

    login_data = {
        'loginName': 'YourStudentID',  # 替换为您的用户名
        'loginPwd': js.call('encoder', 'YourPassword'),  # 替换为您的密码
        'verifyCode': str.upper(captcha_rst),
        'vtoken': token,
        'secretKey': None
    }

    response = session.post(login_url, data=login_data)

    if response.json()["code"] != '1':
        timestamp = response.json()["timestamp"]
    else:
        break

course_list_response = session.get(course_url)
soup = BeautifulSoup(course_list_response.text, 'html.parser')
token = soup.find_all(id="csrfToken")[0].attrs["value"]
course_data_list = [
    {
        "bjdm": "20231-003-PEDU733002-1682320788959",
        "lx": 9,
        "bqmc": "射艺",
        "csrfToken": token,
    },
    {
        "bjdm": "2023202401COMP635001.01",
        "lx": 9,
        "bqmc": "游戏化思维与人文|游戏化思维与人文2023202401COMP635001.01",
        "csrfToken": token,
    }
]

cnt = 0
while cnt < 1000 and len(course_data_list) > 0:
    for course_data in course_data_list:
        response = session.post(choice_course_url + str(execjs.eval("(new Date).getTime()")),
                            data=course_data)
        rst = response.json()
        if rst['code'] == 0:
            print(course_data['bqmc'] + ': ' + rst['msg'])
            cnt += 5
            time.sleep(0.05)
        else:
            course_data_list.remove(course_data)
