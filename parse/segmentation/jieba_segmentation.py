# -*- coding: utf-8 -*-


from parse.dao.blog_dao import *


class JiebaSeg():
    def __init__(self):
        pass

    def get_blogs(self):
        blog_dao = BlogDao()
        blogs = blog_dao.search_all_blogs()
        for blog in blogs:
            print blog[4]