#! /usr/bin/python
#! coding: utf-8

import os
import codecs

def Blog_title():
    bname = []
    btitle = []
    bdate = []

    blog_list = os.listdir("static/content")
    for blog in blog_list: #获得文章的名称、标题和日期，并从最新开始排列
        bname.insert(0,blog[11:-3]) 
        bdate.insert(0,blog[0:10]) 
        f = codecs.open("static/content/" + blog, 'r', 'utf-8')
        btitle.insert(0,f.readline().replace('\r','').replace('\n',''))

    year_temp = '3000' #虚拟一个不会经历的年份
    title_html = "<ul class=\"postsList\">"
    for i in range(len(bname)):
        year_now = bdate[i][0:4]
        if int(year_now) < int(year_temp): #如果有年份小于前一个年份的就加上新的年份标签并显示
            year_temp = year_now
            title_html += '<p class=year>' + year_now + '</p>' #添加显示的年份
        title_html += '<li><a href="/' + bdate[i].replace('-','/') + '/' + bname[i] + "\">" +  btitle[i] + "</a><span id='date'>" + bdate[i] + "</span></li>"
    title_html +="</ul>"
    
    return title_html
