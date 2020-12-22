# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:12:47 2020

@author: 菠萝蜜
"""

import requests
import time
import json

# 自由选课
url = 'http://urp.cup.edu.cn/student/courseSelect/freeCourse/courseList'

# 请求体
datas = {
    'searchtj':'', 'xq':'0', 'jc':'0', 'kclbdm':''
}

# 请求头 需要更改[insert_cookie 和 JSESSIONID]
headers = {
    'Host' : 'urp.cup.edu.cn',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept' : '*/*',
    'Accept-Language' : 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding' : 'gzip, deflate',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With' : 'XMLHttpRequest',
    'Origin' : 'http://urp.cup.edu.cn',
    'DNT' : '1',
    'Connection' : 'keep-alive',
    'Referer' : 'http://urp.cup.edu.cn/student/courseSelect/freeCourse/index?fajhh=4262',
    'Cookie': 'insert_cookie=xxxx; selectionBar=1293218; JSESSIONID=xxxx'    
}

def logger(m):
	with open('longestime.log', 'a', encoding='utf-8') as f:
		f.write(m + '\n')

# 用请求的方式确定 life
i=0
while True:
    try:
        r = requests.post(url, headers=headers, data=datas)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        j = json.loads(r.text)
        logger('请求成功！ '+'i='+str(i)+" "+time.asctime( time.localtime(time.time())))
    except:
        logger('请求失败。。。 '+'i='+str(i)+" "+time.asctime( time.localtime(time.time())))
        break
    
    time.sleep(60 * i)
    i += 1

