#爱企查京东e卡库存监控
#push推送，适用于青龙面板
'''
cron: 10 * * * *
new Env('爱企查e卡监控');
'''
from requests import get, post
from random import choice
import os
import json
import requests
def get_ua(brower_name):
    url = 'https://ghproxy.com/https://raw.githubusercontent.com/farmaster/my/main/master/user-agent.json'
    useragent = choice(get(url).json()[brower_name])
    return useragent
        
def plus(title, content):
    try:
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_TOKEN,
            "title": title,
            "content": content
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

 
def randomstr(numb):
    str = ''
    for i in range(numb):
        str = str + choice('abcdefghijklmnopqrstuvwxyz0123456789')
    return str
def get_status():
    url = 'https://aiqicha.baidu.com/usercenter/getBenefitStatusAjax'
    headers = {
      'User-Agent': get_ua('Safari'),
      'Referer': f'https://aiqicha.baidu.com/m/usercenter/exchangeList?VNK={randomstr(8)}'
    }
    if get(url, headers=headers).json()['data']['AQ03008'] == 1:
        print('E卡有货')
        plus('爱企查E卡监控', '爱企查京东e卡有货')
    else:
        print('E卡无货')
        #plus('爱企查E卡监控', '爱企查京东e卡无货')
if __name__ == '__main__':
    PUSH_TOKEN = ''
    get_status()
