import datetime
import json
import os
import sys

import requests,base64

# global msg
# msg = ""
KEY_OF_COOKIE = "Phone"


def logout(self):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self))
    sys.stdout.flush()


# push推送
PUSH_PLUS_TOKEN = ''
QYWX_KEY = '4df16971-ed23-4549-ac1f-b79b55d19333'

def push_plus_bot(title, content):
    try:
        print("\n")
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'https://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content,
            "topic": ""
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

def qyw(title, content):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={QYWX_KEY}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {'content': f'{title}\n\n{content}'}
    }
    response = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15).json()
    if response['errcode'] == 0:
       print('这是一条通知哦，貌似成功了！')
    else:
       print('消息发送失败，请检查配置文件！')




def telecom_task(mobile):
    print(mobile + " 开始执行任务...")
    base64_mobile = str(base64.b64encode(mobile[5:11].encode('utf-8')), 'utf-8').strip(r'=+') + "!#!" + str(
        base64.b64encode(mobile[0:5].encode('utf-8')), 'utf-8').strip(r'=+')
    h5_headers = {"User-Agent": "CtClient;9.2.0;Android;10;MI 9;" + base64_mobile}
    # 获取用户中心
    home_info_body = requests.get(url="http://49.232.124.89:8080/telecom/getHomeInfo", params={"mobile": mobile}).json()
    home_info_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/homeInfo", json=home_info_body,
                                  headers=h5_headers).json()
    if home_info_ret['resoultMsg'] != "成功":
        print(home_info_ret['resoultMsg'])
        return
    user_id = home_info_ret['data']['userInfo']['userThirdId']
    old_coin = home_info_ret['data']['userInfo']['totalCoin']

    # 签到
    sign_body = requests.get(url="http://49.232.124.89:8080/telecom/getSign", params={"mobile": mobile}).json()
    sign_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/sign", json=sign_body,
                             headers=h5_headers).text
    print(sign_ret)

    # 每日分享任务
    share_body = requests.get(url="http://49.232.124.89:8080/telecom/getShare",
                              params={"mobile": mobile, "userId": user_id}).json()
    requests.post(url="https://appfuwu.189.cn:9021/query/sharingGetGold", json=share_body,
                  headers={"User-Agent": "Xiaomi MI 9/9.2.0"}).text

    # 获取用户中心
    home_info_ret = requests.post(url="https://wapside.189.cn:9001/jt-sign/api/home/homeInfo", json=home_info_body,
                                  headers=h5_headers).json()
    new_coin = home_info_ret['data']['userInfo']['totalCoin']
    print("领取完毕, 现有金豆: " + str(new_coin))
    print("本次领取金豆: " + str(new_coin - old_coin))
    return "【" + str(mobile) + "】" + "领取完毕, 现有金豆: " + str(new_coin) + "，本次领取金豆: " + str(new_coin - old_coin) + "\n"


if __name__ == '__main__':
    Phone = os.environ[KEY_OF_COOKIE]
    cookieList = Phone.split("&")
    logout("检测到{}个账号记录\n开始签到".format(len(cookieList)))
    index = 0
    msg = ""
    for phoneNum in cookieList:
        msg += telecom_task(phoneNum)
        index += 1
   # push_plus_bot("电信签到结果：", msg)
    qyx("电信签到结果：", msg)
    print(msg)
