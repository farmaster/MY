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

def get_ua(brower_name):
    url = 'https://ghproxy.com/https://github.com/farmaster/-/blob/main/user-agent.json'
    useragent = choice(get(url).json()[brower_name])
    return useragent        
        
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
        print('京东50E卡有货,正在推送！')
        os.system("notify '爱企查E卡监控' '京东50E卡有货'")
    else:
        print('京东50E卡无货，已跳过通知推送！')
       # os.system("notify '爱企查E卡监控' '京东50E卡无货'")

if __name__ == '__main__':
    get_status()
