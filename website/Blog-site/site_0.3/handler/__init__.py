#!/usr/bin/python
#!coding=utf-8

import tornado.web
import os

import index
import categories
import tags
import blog

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler): #基本请求
    def get(self):
            self.render("index.html", Blog_title = index.Blog_title() + '\n' + index.Get_tag(), Last_date = index.Last_date())

class CategoriesHandler(tornado.web.RequestHandler): #目录请求
    def get(self):
        self.render("index.html", Blog_title = categories.Blog_title(), Last_date = index.Last_date())  

class ShowTagsHandler(tornado.web.RequestHandler): #标签请求
    def get(self):
        self.render("index.html", Blog_title = index.Get_tag() + '\n' + tags.Blog_title(), Last_date = index.Last_date())

class ShowBlogHandler(tornado.web.RequestHandler): #博客请求
    def get(self,Path):
        Path = Path.replace('/','-')
        file_Path = 'static/content/' + Path + '.md'
        blog_content = blog.Tomarkdown(file_Path)
        if blog_content == 404 :
            self.send_error(404)
            return 0

        [name, title, date, tags] = blog.Get_Name_Title_Date_Tag(file_Path) #获得博客名称、标题、日期、标签
        [previous_blog, next_blog]  = blog.Get_p_n(file_Path)
        self.render("blog.html", Blog_title = title, Blog_content = blog_content , Last_date = index.Last_date(), Blog_time = date, p_blog = previous_blog, n_blog = next_blog, tag = tags )

class AboutHandler(tornado.web.RequestHandler): #about请求
    def get(self):
        self.render("blog.html", Blog_title = "ABOUT", Blog_content = blog.Tomarkdown("static/about.md"), Last_date = index.Last_date(), Blog_time = "", p_blog = "", n_blog = "", tag = "")
