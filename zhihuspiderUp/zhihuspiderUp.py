
# coding=utf-8
from weibo import APIClient
import webbrowser
import pymysql,re,time
import os
import requests
import json
import time
import csv
import os
import codecs
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
APP_KEY='757112173'
APP_SECRET='0d096ef25b49ecb931e806d0cc7a558b'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
# callback url

path = os.getcwd()+"/weibo.csv"
csvfile = open(path, 'w')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
writer.writerow(('created_at','id','text','province'))
#在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：
#利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
print url
webbrowser.open_new(url)

#获取code=后面的内容
print '输入url中code后面的内容后按回车键：'
code = raw_input()
#code = your.web.framework.request.get('code')
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in

# 设置得到的access_token
client.set_access_token(access_token, expires_in)
#可以打印下看看里面都有什么东西
test = client.statuses.user_timeline.get()
print test
#statuses = client.statuses__friends_timeline()['statuses'] #获取当前登录用户以及所关注用户（已授权）的微博
comment_num = 1
i = 1

while True:
    r = client.comments.show.get(id = 4301099668738328,count = 200,page = i) #pgone 回应微博
    if len(r.comments):
        print 'liqiqqqqqqqqqqqqqqq'
        print len(r.comments)
        print 'liqiqqqqqqqqqqqqqqq'
        print '第 %s 页' % i
        for st in r.comments:
            print '第 %s 条评论' % comment_num
            created_at = st.created_at
            comment_id = st.id
            text = st.text
           # source = re.sub('<.*?>|</a>','',str(st.source))
            user_name = st.user.screen_name
            followers = st.user.followers_count
            follow = st.user.friends_count
            province = st.user.province
            print created_at
            print comment_id
            print text
            text = text.lstrip('回复')
           # print source
            #print '评论者：%s,粉丝数：%s,关注数：%s,所在省份编号：%s' % (user_name,followers,follow,province)
            #print '\n'
            print province
            writer.writerow((created_at, comment_id,json.dumps(text, encoding="UTF-8", ensure_ascii=False), province))
           # conn = pymysql.connect(host='127.0.0.1',user='root',password='123456',charset='utf8',use_unicode=False)
           # cur = conn.cursor()
           # sql = "insert into weibo.test(created_at,comment_id,text,source,user_name,followers,follow,province) values(%s,%s,%s,%s,%s,%s,%s,%s)"
           # param = (created_at,comment_id,text,source,user_name,followers,follow,province)
            #try:
            #    A = cur.execute(sql,param)
            #    conn.commit()
            #except Exception,e:
            #    print(e)
            #    conn.rollback()
            comment_num+=1

        i+=1
        time.sleep(4)
    else:
        break