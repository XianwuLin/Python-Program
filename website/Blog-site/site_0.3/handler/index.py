#! /usr/bin/env python
#! coding: utf-8

import os
import codecs
import time

def Last_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def Blog_title():
    bname = []
    btitle = []
    bdate = []
    total = 0

    blog_list = os.listdir("static/content")
    for blog in blog_list: #获得文章的名称、标题和日期，并从最新开始排列
        bname.insert(0,blog[11:-3]) 
        bdate.insert(0,blog[0:10]) 
        f = codecs.open("static/content/" + blog, 'r', 'utf-8')
        btitle_temp = f.readline().replace('\r','').replace('\n','') #去除不同平台下的换行符
        btitle.insert(0,btitle_temp) #f.readline().strip('\r\n')) #去除win下的换行符
        total += 1

    title_html = '<ul class="postsList">'
    for i in range(5):
        title_html += '<li><a href="/' + bdate[i].replace('-','/') + '/' + bname[i] + '">' +  btitle[i] + '</a><span id="date">' + bdate[i] + '</span></li>'
    title_html += '<li><a href="' + '/categories">' + u'所有文章→' + '</a><span id="date">' + str(total) + ' POST</span><li>'
    title_html +="</ul>"
    
    return title_html

def Get_tag():
    '''获得整篇博客的tag标签'''
    tags=[]
    tag_s=[]

    blog_list = os.listdir("static/content")
    for blog in blog_list: #获取博客标签(#vim)
        f = codecs.open("static/content/" + blog, 'r', 'utf-8')
        tag_temp = f.readlines()[-1].replace('\r','').replace('\n','')
        tags += tag_temp.split(",")

    for i in tags:
        tag_s.append((i,tags.count(i)))

    tag = list(set(tag_s)) #去重
    tag.sort(key = tag_s.index) #排序

    tag_html = '<div class="tag-cloud"><span>'
    for i in range(len(tag)):
        tag_html +='<a href="/tags/#' + tag[i][0][1:] + '">' + tag[i][0][1:] + '<span class="tag_num"><sup>' + str(tag[i][1]) + '</sup><span></a>&nbsp;&nbsp;&nbsp;'
    tag_html += '</span></div>'

    return tag_html
