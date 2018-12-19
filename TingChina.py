# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 03:01:08 2018

@author: fuwen

"""
from subprocess import call
import requests,re,time,os


BookID = 27776
BookUrl = 'http://www.tingchina.com/yousheng/disp_%d.htm'%(BookID)
FilePath = r'D:\有声小说\将夜_酸闲人田不辣'

#使用IDM下载
IdmPath = 'C:\idman_lv\IDMan.exe'
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n'])

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
        Url = re.findall('href="%d(.*?)">'%BookID,i)[0]
        Url = Url.replace('/','')
        DetailUrl = 'http://m.tingchina.com/detail' + Url
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
            IdmDownLoad(DownloadUrl, Mp3Name)
            print('%s正在下载……'%Mp3Name)
            time.sleep(2)