# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/zsh/PycharmProjects/graduation')
from dao.blog_dao import *
import jieba
from nltk.probability import FreqDist
import jieba.analyse

class JiebaSeg():
    def __init__(self):
        # type: () -> object
        pass

    def get_segmention_for_blog(self,blog):
        # 开启jieba分词
        jieba.enable_parallel()
        return jieba.cut(blog)
    def get_segmention_for_all_blogs(self):
        blog_dao = BlogDao()
        blogs = blog_dao.search_all_blogs()
        full_blog_info = u""
        for blog in blogs:
            blog_info = blog[4]
            full_blog_info += blog_info
            print blog_info
            print full_blog_info
            # tags = jieba.analyse.extract_tags(blog_info, topK=5, withWeight=False, allowPOS=())
            # print ','.join(tags)
            # print type(blog_info)
        print full_blog_info


