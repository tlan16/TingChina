# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 03:01:08 2018

@author: fuwen

"""
from subprocess import call
from bs4 import BeautifulSoup
import requests,re,time


VideoID = 29169

headers = {
    'Host': 'm.tingchina.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://m.tingchina.com/detailplay_28346_1.htm',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'UM_distinctid=165a386881c364-01ac2a1219e61c4-1a262c32-100200-165a386881d75; ASPSESSIONIDCASTTRAA=PEGNHJADDDCJMCGIDJGEILNE; ASPSESSIONIDCATQSRAB=OEIKFFNDCHKBBIECBHBIHENM'
    }
# 通过主连接生成文件列表
def GetPlaylist(url):
    Playdict = {}
    response = requests.get(url,headers =headers)
    response.encoding = 'gbk'
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')
    PlayList = soup.find_all('div',class_='catalogue')[0]
    PlayList = str(PlayList).split('</a>')
    FirstPlay = PlayList[0].split('">')
    FirstPlayName = FirstPlay[2].split(' ')[0]
    FirstPlayUrl = FirstPlay[1].split('="')[1]
    Playdict[FirstPlayName] = 'http://m.tingchina.com/' + FirstPlayUrl
    for Play in PlayList[1:]:
        Play = Play.split('">')
        try:
            Playname = Play[1]
        except:
            break
        Playurl = 'http://m.tingchina.com/' + Play[0].split('"')[1]
        Playdict[Playname] = Playurl
    return Playdict
#使用IDM下载
IdmPath = 'C:\idman_lv\IDMan.exe'
def IdmDownLoad(DownloadUrl):
    DownPath = r'D:\\'
    call([IdmPath, '/d',DownloadUrl,'/n'])
    
HtmlUrl = 'http://m.tingchina.com/detailplay_%d_0.htm' % VideoID
Playdict = GetPlaylist(HtmlUrl)
Mp3Names= Playdict.keys()

NO = 0
for Mp3Name in Mp3Names:
    NO+=1
    if NO > 0:#在此章节中断，继续下载
        Mp3Url = Playdict[Mp3Name]
        response = requests.get(Mp3Url,headers =headers)
        response.encoding = 'gbk'
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'lxml')
        scripts = soup.find_all('script')
        for script in scripts:
            playlist = re.findall(r'(file:.*)"\r\n',str(script.string),re.S)
            if playlist:
                playlist = ''.join(playlist[0].split())
                playlist = playlist.replace('"','')
                playlist = playlist.split(',')
                DownloadUrl = playlist[0].replace('file:','')
                Name = playlist[1].replace('trackName:','')
                with open('UrlList.txt','a') as f:
                    IdmDownLoad(DownloadUrl)
                    time.sleep(5)
    else:
        print('第%d章节已下载，跳过'%NO)
