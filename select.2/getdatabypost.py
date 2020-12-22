# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 20:33:56 2020

@author: 菠萝蜜
"""

import requests
import json
import pandas as pd
import time

import  smtplib
from email.mime.text import MIMEText 
from email.header import Header 

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
    'Referer' : 'http://urp.cup.edu.cn/student/courseSelect/freeCourse/index?fajhh=4262'
}

# =============================================================================
mail_host="smtp.qq.com"  #设置服务器
mail_user="3510443958@qq.com"    #用户名
mail_pass="secret"   #口令 
sender = '3510443958@qq.com'
# =============================================================================

def getHTMLText():
    try:
        cookie = 'insert_cookie={}; selectionBar=1293218; JSESSIONID={}'.format(getinfo('cookie'),getinfo('session'))
        headers['Cookie'] = cookie
        r = requests.post(url, headers=headers, data=datas)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

r = getHTMLText()

def parseText(r):
    try:
        return json.loads(r)
    except:
        return ''

def getCourses(j):
    return j['rwRxkZlList']

def logger(msg):
    with open('whathappened.log', 'a', encoding='utf-8')as f:
        now = time.asctime( time.localtime(time.time()) )
        f.write('[' + now + '] ' + msg + '\n')

def keepData(clist):
    kcm = [] # 课程号
    kch = [] # 课程名
    kxh = [] # 课序号
    skjs = [] # 上课教师
    kyl =[] # 课余量
    krl=[] # 课容量
    for c in clist: # type(c) = dict
        # print(c['kcm'],c['kch'],c['kxh'],c['skjs'])
        kcm.append(c['kcm'])
        kch.append(c['kch'])
        kxh.append(c['kxh'])
        skjs.append(c['skjs'])
        kyl.append(c['bkskyl'])
        krl.append(c['bkskrl'])
    d = {'课程名':kcm, '课余量':kyl, '课程号':kch, '上课教师':skjs, '课序号':kxh, '课容量':krl }
    df = pd.DataFrame(d)
    now = time.asctime( time.localtime(time.time()))
    fn = 'courstlist_' + now.replace(' ','-').replace(':',')') + '.xlsx'
    df.to_excel(fn, index=False)
    logger('数据保存成功')

def sendEmail(info): # [{'':''},{}]
    e = getinfo('email')
    msg = '<h3>我是一个没得感情的机器人~~~，主人，你要的数据在下:</h3>'
    msg += '<table border="1"><tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>'.format('课程名','课余量','课程号','上课教师','课序号')
    for c in info:
        msg += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(c['课程名'],c['课余量'],c['课程号'],c['上课老师'],c['课序号'])
    msg += '</table>'
    # 发送
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = Header("gyjの选课py脚本", 'utf-8')
    message['To'] =  Header("", 'utf-8')
     
    subject = '选课信息更新'
    message['Subject'] = Header(subject, 'utf-8')
     
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, e, message.as_string())
        logger("Succ: 邮件发送成功")
        smtpObj.quit() # terminate session
    except smtplib.SMTPException:
        logger("Error: 无法发送邮件")

def sendQuitEmail():
    e = getinfo('email')
    msg = '<h3>非常不幸~~，连接断开~~，孩子不能为您服务了┭┮﹏┭┮</h3>'
    # 发送
    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = Header("gyjの选课py脚本", 'utf-8')
    message['To'] =  Header("", 'utf-8')
     
    subject = '选课连接断开'
    message['Subject'] = Header(subject, 'utf-8')
     
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, e, message.as_string())
        logger("Succ: 邮件发送成功")
        smtpObj.quit() # terminate session
    except smtplib.SMTPException:
        logger("Error: 无法发送邮件")

def getWantedData(clist):
    # 读取课程号，获得 【课程名、课余量、课容量、课程号、课序号、上课老师】
    l = getinfo('kch')
    lm = getinfo('kcm')
    info = []
    for c in clist:
        if c['kch'] in l or isAlike(c['kcm'], lm) : # 课程号匹配或课程名模糊匹配
            d = {}
            d['课程名'] = c['kcm']
            d['课余量'] = c['bkskyl']
            d['课程号'] = c['kch']
            d['课序号'] = c['kxh']
            d['上课老师'] = c['skjs']
            info.append(d)
    return info

# 日语文化 in 日语文化专题  -- True
def isAlike(km, lm):
    for m in lm:
        if m in km:
            return True
    return False

def getinfo(k):
    typelist1 = ['cookie', 'session']
    typelist2 = ['kch', 'kcm', 'email']
    l = []
    with open('getinfo.txt', 'r', encoding='utf-8')as f:
        l = f.readlines()
    d = {}
    for i in l:
        j = i.replace('\n', '') # 'cookie 123'
        kv = j.split(' ')
        if len(kv) == 2:
            d[kv[0]] = kv[1]
    if k in typelist1:
        return d[k]
    if k in typelist2:
        return d[k].split(',')
    return ''

def main(i):    # 第几次
    # 获取请求文本
    r = getHTMLText()
    # 获取 json对象
    j = parseText(r) # {"":"[{},{},,,{}]"}
    if len(j) == 0:
        logger('连接已断开，程序退出')
        return -1
    # 获取课程列表
    courselist = parseText(getCourses(j)) # list contains dict
    # 保存数据
    keepData(courselist)
    # 获取要发送的数据
    info = getWantedData(courselist)
    sendEmail(info) # 发送查询到的信息
    logger('Over: 结束')
    logger(str(i) + ' done!')
    return 1

if __name__ == '__main__':
    i=0
    m=10 # 五分钟连接并查询一次 ===> 保持会话
    while True:
        r = main(i) # 一次数据请求
        if r == -1:
            sendQuitEmail() # 发送邮件，报告退出
            break
        i += 1
		#break  # 只测试便可
        time.sleep(60 * m)


# =============================================================================
# 
#     j = json.loads(r.text) # 2json
#     info = j['rwRxkZlList']
#     with open('list.json', 'w', encoding='utf-8')as f:
#         f.write(info)
#     cl = json.loads(info) # 2json
#     kcm = []
#     kch = []
#     kxh = []
#     skjs = []
#     kyl =[]
#     krl=[]
#     for c in cl:
#         # print(c['kcm'],c['kch'],c['kxh'],c['skjs'])
#         kcm.append(c['kcm'])
#         kch.append(c['kch'])
#         kxh.append(c['kxh'])
#         skjs.append(c['skjs'])
#         kyl.append(c['bkskyl'])
#         krl.append(c['krl'])
#     d = {'课程号':kch, '课序号':kxh, '课程名':kcm, '课余量':kyl, '课容量':krl,'上课教师':skjs }
#     df = pd.DataFrame(d)
#     df.to_excel('courstlist.xlsx', index=False)
#     print("done!")
# else:
#     print('failed')
# # =============================================================================

# =============================================================================
#     print(r.text)
#     with open('courstlist.json', 'w')as f:
#         f.write(r.text)
# =============================================================================


# =============================================================================
# {
#     "bkskrl": 66,                  课容量
#     "bkskyl": -4,                  课余量
#     "cxjc": "2",
#     "id": "434",
#     "jasm": "206",
#     "jxlm": "四教",                 教学楼名
#     "kch": "100305T070",           课程号
#     "kclbdm": "1",
#     "kclbmc": "本科",               课程类别名称
#     "kcm": "污染控制工程",            课程名
#     "kkxqh": "1",                   开课学区号
#     "kkxqm": "校本部",               开课学区名
#     "kkxsh": "03",
#     "kkxsjc": "化学工程与环境学院",
#     "kslxdm": "",
#     "kslxmc": "",
#     "kxh": "01",                     课序号
#     "sflbdm": "",
#     "sfxzskyz": "",
#     "sfxzxdlx": "是",
#     "sfxzxslx": "",
#     "sfxzxsnj": "",
#     "sfxzxsxs": "",
#     "sfxzxxkc": "",
#     "sjdd": [{                 上课地点
#         "cxjc": "2", 
#         "jasm": "206",
#         "jxlm": "四教",
#         "skjc": "3",
#         "skxq": "1",
#         "skzc": "000000001111111100000000",
#         "xqm": "校本部",
#         "zcsm": "9-16周"
#     }, {
#         "cxjc": "2",
#         "jasm": "307",
#         "jxlm": "四教",
#         "skjc": "5",
#         "skxq": "3",
#         "skzc": "000000001111111100000000",
#         "xqm": "校本部",
#         "zcsm": "9-16周"
#     }],
#     "skjc": "3",
#     "skjs": "阎光绪* ",                  上课教师
#     "skxq": "1",                        上课学期
#     "skzc": "000000001111111100000000",
#     "xf": 2,                            学分
#     "xkbz": "",
#     "xkkzdm": "01",
#     "xkkzh": "",
#     "xkkzsm": "可选可退",                 选课控制说明
#     "xkmsdm": "02",
#     "xkmssm": "志愿式",                 选课模式说明
#     "xkxzsm": "允许修读类型 主修\r\n;",                 选课限制说明
#     "xqm": "校本部",                      学区名
#     "xs": 32,                           学时
#     "zcsm": "9-16周",                  
#     "zxjxjhh": "2020-2021-2-2"
# }
# =============================================================================

#[STMP发邮件] https://www.runoob.com/python/python-email.html
#str.format https://www.runoob.com/python/att-string-format.html




