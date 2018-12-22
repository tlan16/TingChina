# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 21:58:12 2018

@author: fuwen
"""
from bs4 import BeautifulSoup
from subprocess import call
import requests,re,time,os

BookUrl = 'http://www.tingchina.com/xiaohua/disp_246.htm'
FilePath = r'D:\有声小说\隋唐演义(130回电台版)'


IdmPath = 'C:\idman_lv\IDMan.exe'

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'UM_distinctid=165a386881c364-01ac2a1219e61c4-1a262c32-100200-165a386881d75; bdshare_firstime=1536046827957; t_play_url=http%3A//www.tingchina.com/yousheng/28024/play_28024_0.htm; jieshaoren=0; ASPSESSIONIDQSDRABQT=OFEFMKOBGFCFLNBJOJBIOKID; CNZZDATA1497416=cnzz_eid%3D533340621-1536043618-%26ntime%3D1545385285; cscpvrich2729_fidx=1; cscpvcouplet8854_fidx=1; t_play_mode=real',
    'Host':'www.tingchina.com',
    'Referer':'http://www.tingchina.com/yousheng/28024/play_28024_0.htm',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }
Bookid = re.findall('(\d+)',BookUrl)[0] 
#使用IDM下载
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n'])

#获取每集名称    
def GetMp3NameList(BookUrl) :    
    response = requests.get(BookUrl)   
    response.encoding = 'gb2312'    
    html_doc = response.text    
    Soup = BeautifulSoup(html_doc,'html5lib')    
    MainSoup = Soup.find_all('div',class_ = 'list')[0]    
    TitleUrl = MainSoup.find_all('li',class_ = False)    
    TitleUrl = MainSoup.find_all('li',class_ = False) 
    Mp3nameList = [s.text for s in TitleUrl]
    Mp3nameList = [j.replace('NO','') for j in Mp3nameList]
    return Mp3nameList
  
#获取分类、书籍名称（有声） 
def GetDetail(BookUrl):
    response = requests.get(BookUrl)
    response.encoding = 'gb2312'
    html_doc = response.text
    flei =  re.findall('htm">(.*?)</a> >',html_doc)[0]
    bookname = re.findall("var pl_bookname='(.*?)';",html_doc)[0]
    return flei, bookname

# 获取分类、书籍名称（评书）
def Getdetail(BookUrl):
    response = requests.get(BookUrl)
    response.encoding = 'gb2312'
    html_doc = response.text
    Soup = BeautifulSoup(html_doc,'lxml')
    p = Soup.select('body > div.wrap03.clearfix > div.main03 > div > div.book01.padding10 > img')[0]
    p = re.findall('src="/cover/pingshu/(.*?).gif"',str(p))[0]
    flei = p.split('_')[-1]
    bookname = p.replace('_'+flei,'')
    return flei, bookname

#获取书籍名称（相声）
def Getbookname(BookUrl):
    response = requests.get(BookUrl)
    response.encoding = 'gb2312'
    html_doc = response.text
    Soup = BeautifulSoup(html_doc,'lxml')
    bookname = Soup.find_all('strong')[0]
    bookname = bookname.text
    return bookname    

#获取书籍名称（戏曲）
def GetFenlei():
    response = requests.get(BookUrl)
    response.encoding = 'gb2312'
    html_doc = response.text
    Soup = BeautifulSoup(html_doc,'lxml')    
    p = Soup.select('body > div.wrap03.clearfix > div.main01 > dl.category.on > dd > ul > li:nth-of-type(2) > a')[0]
    flei = re.findall('htm">(.*?)</a>',str(p))[0]
    return flei

if 'yousheng' in BookUrl :
    print('正在抓取有声小说分类……')
    flei, bookname = GetDetail(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/yousheng/flash.asp?id=%s&inum=1&flei=%s&bookname=%s&filename=%s'%(Bookid, flei, bookname, filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t33.tingchina.com/yousheng/%s/%s/%s?key=%s'%(flei, bookname, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)
    
elif 'pingshu' in BookUrl :
    print('正在抓取评书分类……')
    flei, bookname = Getdetail(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/pingshu/flash.asp?id=%s&inum=1&flei=%s&bookname=%s&filename=%s'%(Bookid,flei, bookname, filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t33.tingchina.com/pingshu/%s/%s/%s?key=%s'%(flei, bookname, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)

elif 'xiqu' in BookUrl :
    print('正在抓取戏曲分类……')
    FileName = GetMp3NameList(BookUrl) 
    flei = GetFenlei()
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/xiqu/geturl.asp?id=%s&flei=%s&filename=%s'%(Bookid,flei,filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t33.tingchina.com/xiqu/%s/%s?key=%s'%(flei, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)

elif 'jiaoyu' in BookUrl :
    print('正在抓取教育分类……')
    bookname = Getbookname(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/jiaoyu/geturl.asp?id=%s&bookname=%s&filename=%s'%(Bookid, bookname, filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t33.tingchina.com/jiaoyu/%s/%s?key=%s'%(bookname, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)
    
elif 'erge' in BookUrl :
    print('正在抓取儿歌分类……')
    bookname = Getbookname(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/erge/geturl.asp?id=%s&bookname=%s&filename=%s'%(Bookid, bookname, filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t33.tingchina.com/erge/%s/%s?key=%s'%(bookname, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)

elif 'xiangsheng' in BookUrl :
    print('正在抓取相声分类……')
    bookname = Getbookname(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
        JsUrl = 'http://www.tingchina.com/play/xiangsheng/flash.asp?id=%s&filename=%s/%s'%(Bookid,bookname,filename)
        Response = requests.get(JsUrl, headers = headers)
        Html_doc = Response.text
        Downkey = re.findall('key=(.*?)";',Html_doc)[0]
        DownUrl = 'http://t44.tingchina.com/xiangsheng/%s/%s?key=%s'%(bookname, filename, Downkey)
        IdmDownLoad(DownUrl, filename)
        time.sleep(2)
elif 'xiaohua' in BookUrl :
    print('正在抓取笑话分类……')
    bookname = Getbookname(BookUrl)
    FileName = GetMp3NameList(BookUrl)
    for filename in FileName :
        if filename :
            pass
        else :
            continue
    JsUrl = 'http://www.tingchina.com/play/xiaohua/geturl.asp?id=%s&bookname=%s&filename=%s'%(Bookid, bookname, filename)
    Response = requests.get(JsUrl, headers = headers)
    Html_doc = Response.text
    Downkey = re.findall('key=(.*?)";',Html_doc)[0]
    DownUrl = 'http://t33.tingchina.com/xiaohua/%s/%s?key=%s'(bookname, filename, Downkey)
    IdmDownLoad(DownUrl, filename)
    time.sleep(2)    
    
else :
    print('暂不支持此分类……')