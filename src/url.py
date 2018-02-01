#!/usr/bin/python2.7
#!-*- coding:UTF-8 -*-

import urllib
import re
import json
import math
import time
import logging

filelog="../log/logger.log"
logging.basicConfig(filename = filelog, level = logging.DEBUG)  
logging.debug("this is a debug msg!")
logging.info("this is a info msg!")
logging.warn("this is a warn msg!")
logging.error("this is a error msg!")
logging.critical("this is a critical msg!")
fod=open("../data/pa.txt",'ab')
foc1=open("../conf/one.txt",'w')
print "注意！时间格式为：年 月 日 时：分：秒"
str1=raw_input("请输入第一个时间：")
str2=raw_input("请输入第二个时间：")
try:
    sr=time.mktime(time.strptime(str1,"%Y %m %d %H:%M:%S"))
except ValueError:
    firsttime=0
else:
        firsttime=sr
try:
    sr=time.mktime(time.strptime(str2,"%Y %m %d %H:%M:%S"))
except ValueError:
    lasttime=10000000000
else:
    lasttime=sr
headers={'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
url1=urllib.urlopen("http://fund.eastmoney.com/js/fundcode_search.js")
out=url1.read()
foc1.write(out)
va=re.search(r"var r =(.*?);",out)
listt=va.group(1)
listtt=json.loads(listt)
array=[]
for i in range(len(listtt)):
    array.append(listtt[i][0])
for i in range(len(array)):
    #request=urllib2.Request(url="http://fund.eastmoney.com/pingzhongdata/"+listtt[i][0]+".js",data=headers,timeout="0.5")
    try:
        url2=urllib.urlopen("http://fund.eastmoney.com/pingzhongdata/"+listtt[i][0]+".js")
    except Exception:
        continue
    else:
        data=url2.read()
    time.sleep(1)
    foc2=open("../conf/"+str(i)+".txt",'w')
    foc2.write(data)
    var=re.search(r"var Data_ACWorthTrend =(.*?);",data)
    if var==None:
        continue
    fod.write(str(var.groups()))
    lists=var.group(1)
    li=json.loads(lists)
    sum=0
    count=0
    lis=[]
    for i in range(len(li)):
        if li[i][0]/1000>firsttime and li[i][0]/1000<lasttime:
            sum+=li[i][1]
            count+=1
            lis.append(li[i])
    fod.write(str(lis))
    avg=sum/count
    for i in range(1,len(lis)):
        for j in range(0,len(lis)-1):
            if math.pow(lis[j][1]-avg,2)>math.pow(lis[j+1][1]-avg,2):
                lis[j],lis[j+1]=lis[j+1],lis[j]
    fod.write(str(lis))
    foc2.close()
url1.close()
fod.close()
foc1.close()
foc2.close()
