#爱企查京东e卡库存监控
#调用系统自带推送，适用于青龙面板
'''
cron: 10 * * * *
new Env('爱企查e卡监控');
'''
from requests import get, post
from random import choice
import os
import json
import requests

def start():
    url = 'https://aiqicha.baidu.com/usercenter/getBenefitStatusAjax'
    headers = {
      'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/522+ (KHTML, like Gecko) Version/3.0.2 Safari/522.12',
      'Referer': 'https://qiye.baidu.com/usercenter',
      'Cookie': ''
    }
    if get(url, headers=headers).json()['data']['AQ03008'] == 1:
        print('京东50E卡有货,正在推送！')
        os.system("notify '爱企查E卡监控' '京东50E卡有货'")
    else:
        print('京东50E卡无货，已跳过通知推送！')
       # os.system("notify '爱企查E卡监控' '京东50E卡无货'")

if __name__ == '__main__':
    start()
