#爱企查京东e卡库存监控
#需要pushplus推送，TOKEN在52行
'''
cron: 10 * * * *
new Env('爱企查e卡监控');
'''
from requests import get, post
from random import choice
import os
import json
import requests

def plus(title, content):
    try:
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('这是一条通知哦，貌似成功了！')
        else:
            print('消息发送失败，请检查TOKEN！')
    except Exception as e:
        print(e)

def start():
    url = 'https://aiqicha.baidu.com/usercenter/getBenefitStatusAjax'
    headers = {
      'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/522+ (KHTML, like Gecko) Version/3.0.2 Safari/522.12',
      'Referer': 'https://qiye.baidu.com/usercenter',
      'Cookie': ''
    }  
    if get(url, headers=headers).json()['data']['AQ03008'] == 1:
      if TOKEN != '':
        print('京东50E卡有货,正在推送！')
        plus('爱企查E卡监控', '京东50E卡有货')
      else:   
        print('京东50E卡有货,TOKEN未输入，推送取消！')
    else:
      if TOKEN != '':
         print('京东50E卡无货，已跳过通知推送！')
          #plus('爱企查E卡监控', '京东50E卡无货')
      else:  
       print('京东50E卡无货！')
       
if __name__ == '__main__':
    TOKEN = ''
    start()
