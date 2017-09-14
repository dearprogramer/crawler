import requests
import re
import urllib.request as rq
import os
import connect
from bs4 import BeautifulSoup
class Directory:
    def __init__(self,base_url,name,encoding='utf-8'):
        self.base_url=base_url
        self.encoding=encoding
        self.now_page=1
        self.name=name
        self.page_list=dict()
        self.__dict__={'base_url':base_url,'name':name}
        self.page_list.append(self.defaut_url)

    def get_content(self,pattern): #get a beautiful soup result
        rsp=self.get_response(self.base_url)
        u=BeautifulSoup(rsp,'html.parser',from_encoding=self.encoding)
        return u


    def get_dirs_result(self,result_dic):  #in order to get a dirs
        dir_list = list()
        for (key,value) in result_dic:
            t_dir=Directory(name=key,url=value,encoding=self.encoding)
            dir_list.append(t_dir)
        return dir_list

    def get_firstpage(self):
        return self.defaut_url

    def get_pagelist(self):
        for i in range(self.maxnum-1):
            self.page_list.append(self.prefix+i+self.subfix)
        return self.page_list

    def get_response(self,r_path):
        path=os.path.join(self.base_url,r_path)
        response=requests.get(url).content
        return response

    def get_node_url(self,pattern,url):
        response=self.get_response(url)
        soup=BeautifulSoup(response,'html.parser',from_encoding=self.encoding)
        content=soup.select('div[class="ui-cnt"]')
        print(content)




def get_response(url):
    response=requests.get(url).content
    return response

def get_content(html):
    soup=BeautifulSoup(html, 'html.parser',from_encoding='gbk')
    content=soup.find_all(href=re.compile(r'/L/'))
    return content

def display(content):
    for it in content:
        it['href']=r'http://www.xinxin30.pw/'+it['href']
        print(it.get('href'))

def save_links(data,filename):
    basepath=r'G:\data'
    path=os.path.join(basepath,filename)
    if not os.path.exists(basepath):
        os.mkdir(basepath)
    with open(path,'w',encoding='utf') as f:
         f.write(data)



url='http://www.xinxin30.pw'
res=get_response(url)
html=get_content(res)
display(html)
s=connect.User(role='admin')
d=connect.datadeal()
l=d.search(s)
for f in l:
    print(f.__dict__)


save_links(str(html),'a.txt')


