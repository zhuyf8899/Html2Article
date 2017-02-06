#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#Html2Article.py:基于统计的正文提取
import urllib  
import urllib2
import zlib
import cookielib
import re
import sys

#如果想通过图表查看文档行长度分布请确保安装numpy和pylab
import numpy as np
import pylab as pl

threshold_of_article = 180  #maybe not good enough.
#Some news example:
#http://news.163.com/17/0205/17/CCHFGSIP000189FH.html
#http://news.sina.com.cn/o/2017-02-06/doc-ifyafenm2867797.shtml
#http://finance.ifeng.com/a/20170206/15180109_0.shtml

def get_html(url):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
    request = urllib2.Request(url=url,headers=headers)
    request.add_header('Accept-encoding', 'gzip,utf-8')
    #print request.headers
    response = opener.open(request)
    html = response.read()
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    re_type = re.compile(r'charset=".*?"')
    char_type = re_type.search(html).group()
    if len(char_type) >= 10:
        #print char_type[9:-1]
        char_type = char_type[9:-1].upper()
    else:
        char_type = "UTF-8"
    #print html

    if html:
        return html.decode(char_type).encode('UTF-8')
    else:
        return None

def html2Article(html_file):
    #首先去除可能导致误差的script和css，之后再去标签
    tempResult = re.sub('<script([\s\S]*?)</script>','',html_file)
    tempResult = re.sub('<style([\s\S]*?)</style>','',tempResult)
    tempResult = re.sub('(?is)<.*?>','',tempResult)
    tempResult = tempResult.replace(' ','')
    tempResultArray = tempResult.split('\n')
    #print tempResult

    data = []
    string_data = []
    result_data = []
    summ = 0
    count = 0

    #计算长度非零行的行数与总长度
    for oneLine in tempResultArray:
        if(len(oneLine)>0):
            data.append(len(oneLine))
            string_data.append(oneLine)
            summ += len(oneLine)
            count += 1
    #print 'averange is:'+ str(summ/count)
    for oneLine in string_data:
        #if len(oneLine) >= summ/count+180:
        if len(oneLine) >= 180:
            print oneLine
            result_data.append(oneLine)

    #画图部分
    #data = np.array(data)
    #x = np.arange(len(data))
    #pl.bar(x, data, alpha = .9, color = 'g')
    #pl.show()

    return result_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python Html2Article.py <article's address>"
        exit(-1)
    try:
        html_data = get_html(sys.argv[1])
    except Exception as e:
        print "Failed to get article by network, details:\n" + str(e)
        exit(-2)
    html2Article(html_data)
