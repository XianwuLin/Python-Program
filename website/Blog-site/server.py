#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import os
import codecs
import time
import misaka as m

#公用函数
def get_tag():
    '''获得整篇博客的tag标签'''
    tags=[]
    tag_s=[]

    blog_list =  sorted(os.listdir("static/content"))
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

def last_date():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def tomarkdown(file_Path):
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
#公用函数


class MainHandler(tornado.web.RequestHandler): #主页请求
    def get(self):
        self.render("index.html", Blog_title = self.Blog_title() + '\n' + get_tag(), Last_date = last_date())

    def Blog_title(self):
        bname = []
        btitle = []
        bdate = []
        total = 0

        blog_list = sorted(os.listdir("static/content"))
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



class CategoriesHandler(tornado.web.RequestHandler): #目录请求
    def get(self):
        self.render("index.html", Blog_title = self.Blog_title(), Last_date = last_date())  

    def Blog_title(self):
        bname = []
        btitle = []
        bdate = []

        blog_list = sorted(os.listdir("static/content"))
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



class ShowTagsHandler(tornado.web.RequestHandler): #标签请求
    def get(self):
        self.render("index.html", Blog_title = get_tag() + '\n' + self.Blog_title(), Last_date = last_date())

    def Blog_title(self):
        bname = []
        btitle = []
        bdate = []
        btags = []
        tags_s=[]

        blog_list = sorted(os.listdir("static/content"))
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



class ShowBlogHandler(tornado.web.RequestHandler): #博客请求
    def get(self,Path):
        Path = Path.replace('/','-')
        file_Path = 'static/content/' + Path + '.md'
        blog_content = tomarkdown(file_Path)
        if blog_content == 404 :
            self.send_error(404)
            return 0

        [name, title, date, tags] = self.Get_Name_Title_Date_Tag(file_Path) #获得博客名称、标题、日期、标签
        [previous_blog, next_blog]  = self.Get_p_n(file_Path)
        self.render("blog.html", Blog_title = title, Blog_content = blog_content , Last_date = last_date(), Blog_time = date, p_blog = previous_blog, n_blog = next_blog, tag = tags )

    def Get_Name_Title_Date_Tag(self,file_Path):
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

    def Get_p_n(self,file_Path):

        now_date = file_Path[15:25]
        bname = []
        btitle = []
        bdate = []

        blog_list = sorted(os.listdir("static/content"))
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



class AboutHandler(tornado.web.RequestHandler): #about请求
    def get(self):
        self.render("blog.html", Blog_title = "ABOUT", Blog_content = tomarkdown("static/about.md"), Last_date = last_date(), Blog_time = "", p_blog = "", n_blog = "", tag = "")



settings = {
            "autoescape":None,
            "static_path": os.path.join(os.path.dirname(__file__), "static"), 
            "template_path":os.path.join(os.path.dirname(__file__), "templates"),
            'debug': True,
                }

define("port", default=8888, help="run on the given port", type=int)

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/(\d{4}/\d{2}/\d{2}/\w+)", ShowBlogHandler),   
        (r"/categories", CategoriesHandler),
        (r"/about", AboutHandler),
        (r"/tags/\S*", ShowTagsHandler),
        ],**settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
