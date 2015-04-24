#! /usr/bin/env python
#! coding: utf-8
import misaka as m
import codecs
import os

def Tomarkdown(file_Path):
    try:
        content = codecs.open(file_Path,'r','utf-8')
        b_md = content.read()
        content.close()
        content = codecs.open(file_Path,'r','utf-8')
        b_md_e = content.readlines()[-1]
        b_md = b_md[:len(b_md)-len(b_md_e)]
    except:
        return 404
    markdown = m.html(b_md , extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
    markdown = markdown.replace('<pre>','<pre class="prettyprint linenums">')
    return markdown

def Get_Name_Title_Date_Tag(file_Path):
    content = codecs.open(file_Path,'r','utf-8')
    b_md = content.readlines()
     
    name = file_Path[26:-3]
    title = b_md[0].replace('\r','').replace('\n','')
    date = file_Path[15:25]
    b_tags = b_md[-1].replace('\r','').replace('\n','')
    b_tag = b_tags.split(',')
    content.close()
    tag_html = ''
    for i in b_tag:
        tag_html += '<a href="/tags/' + i + '">' + i + '</a>&nbsp;&nbsp;&nbsp;'

    return [name, title, date, tag_html]


def Get_p_n(file_Path):

    now_date = file_Path[15:25]
    bname = []
    btitle = []
    bdate = []

    blog_list = os.listdir("static/content")
    for blog in blog_list: #获得文章的名称、标题和日期，并从最新开始排列
        bname.insert(0,blog[11:-3]) 
        bdate.insert(0,blog[0:10]) 
        f = codecs.open("static/content/" + blog, 'r', 'utf-8')
        btitle.insert(0,f.readline())
    now_id = bdate.index(now_date)
    if now_id > 0 and now_id < len(bdate)-1: #中间的博客
        return ['<a href="/' + bdate[now_id + 1].replace('-','/') + '/' + bname[now_id + 1] + '">' + '&larr;&nbsp;' + btitle[now_id + 1] +'</a>',
                '<a href="/' + bdate[now_id - 1].replace('-','/') + '/' + bname[now_id - 1] + '">' + btitle[now_id - 1] + '&nbsp;&rarr;' +'</a>']
    elif now_id == 0: #最新的博客
        return ['<a href="/' + bdate[now_id + 1].replace('-','/') + '/' + bname[now_id + 1] + '">' +'&larr;&nbsp;' + btitle[now_id + 1] +'</a>',
                '']
    elif now_id == len(bdate)-1: #最旧的博客
        return  ['',
                '<a href="/' + bdate[now_id - 1].replace('-','/') + '/' + bname[now_id - 1] + '">' +  btitle[now_id - 1] + '&nbsp;&rarr;' +'</a>']
