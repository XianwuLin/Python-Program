#! /usr/bin/python
#! coding: utf-8

import sqlite3
import os
import codecs

def Blog_title(tag = ""):
    bname = []
    btitle = []
    bdate = []
    btags = []
    tags_s=[]

    blog_list = os.listdir("static/content")
    for blog in blog_list: #获取博客名称、日期、标题、标签(#vim)
        bname.insert(0,blog[11:-3])
        bdate.insert(0,blog[0:10]) 
        f = codecs.open("static/content/" + blog, 'r', 'utf-8')
        ffile = f.readlines()
        btitle.insert(0,ffile[0].replace('\r','').replace('\n',''))
        btags.insert(0,ffile[-1].replace('\r','').replace('\n',''))
        tags_s += btags[0].split(",")
    
    tags = list(set(tags_s)) #去重
    tags.sort(key = tags_s.index) #排序

    tag_html = ''
    for tag in tags:
        tag_html += '<div class="tag_title"><a name="' + tag[1:] + '">' + tag + '</a></div>\n'
        title_html = "<ul class=\"postsList\">"
        for i in range(len(btags)):
            if btags[i].find(tag) != -1:
                title_html += '<li><a href="/' + bdate[i].replace('-','/') + '/' + bname[i] + '">' +  btitle[i] + '</a><span id="date">' + bdate[i] + '</span></li>'
            else:
                continue
        title_html +="</ul>\n"
        tag_html += title_html
    
    return tag_html
