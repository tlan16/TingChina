# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 03:01:08 2018

@author: fuwen

"""
from subprocess import call
import requests,re,time,os,sys
from datetime import datetime
from pprint import pprint
import urllib.request
import urllib.parse

BookID = int(sys.argv[1])
BookUrl = 'http://www.tingchina.com/yousheng/disp_%d.htm'%(BookID)
FilePath = sys.argv[2]


if not BookID or not FilePath:
    sys.exit()

print('started at '+str(datetime.now()))
# time.sleep(1)
# sys.exit()


def Downloader(DownloadUrl, Mp3Name):
    print('Downloading "%s" to "%s" ... '%(DownloadUrl, FilePath+'/'+Mp3Name))
    headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,zh-TW;q=0.5,ja;q=0.4',
        }
    r = requests.get(DownloadUrl,headers=headers)
    pprint(r)
    if 200 == r.status_code and not r.text.startswith('<div'):
        with open(FilePath+'/'+Mp3Name,'wb') as f:
            f.write(r.content)
    else:
        print('Unexpected response %s %s'%(r.status_code, r.text))

response = requests.get(BookUrl)
response.encoding = 'gbk'
html_doc = response.text
html_list = html_doc.split('\n')
BookDict = {}
AlreadyDown = [FileName for FileName in os.listdir(FilePath)]
for i in html_list :
    s = re.findall('play_%s(.*).htm">'%BookID,i)
    if s:
        Name = re.findall('htm">(.*?)<',i)[0]
        if Name in AlreadyDown :
            print('%s已经下载，本集跳过……'%Name)
            continue
        if Name.replace('.mp3','.m4a') in AlreadyDown :
            print('%s已经下载，本集跳过……'%Name.replace('.mp3','.m4a'))
            continue
        Url = re.findall('href="%d(.*?)">'%BookID,i)[0]
        Url = Url.replace('/','')
        DetailUrl = 'http://m.tingchina.com/detail' + Url
        print(DetailUrl)
        BookDict[Name] = DetailUrl
        response = requests.get(DetailUrl)
        response.encoding = 'gbk'
        html = response.text
        playlist = re.findall(r'(file:.*)"\r\n',html,re.S)
        if playlist:
            playlist = ''.join(playlist[0].split())
            playlist = playlist.replace('"','')
            playlist = playlist.split(',')
            DownloadUrl = playlist[0].replace('file:','')
            Mp3Name = playlist[1].replace('trackName:','')
            Downloader(DownloadUrl, Mp3Name)
            time.sleep(2)
            # break