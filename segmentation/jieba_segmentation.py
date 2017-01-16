# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/zsh/PycharmProjects/graduation')
from dao.blog_dao import *
import jieba
from nltk.probability import FreqDist
import jieba.analyse
import  math
import nltk
from numpy import array
class JiebaSeg():
    def __init__(self):
        pass

    def get_segmention_for_blog(self, blog):
        # 开启jieba分词
        jieba.enable_parallel()
        return jieba.cut(blog)

    def get_segmention_for_all_blogs(self):
        jieba.analyse.set_stop_words("/home/zsh/PycharmProjects/graduation/dict/stop_words.txt")
        blog_dao = BlogDao()
        blogs = blog_dao.search_all_blogs()
        full_blog_info = u""
        for blog in blogs:
            blog_info = blog[4]
            # full_blog_info += blog_info
            print blog_info
            segs = jieba.analyse.textrank(blog_info,topK=1000)
            print "/".join(segs)

    def get_top_keywords(self):
        jieba.analyse.set_stop_words("/home/zsh/PycharmProjects/graduation/dict/stop_words.txt")
        blog_dao = BlogDao()
        blogs = blog_dao.search_all_blogs()
        full_blog_info = u""
        # 统计维度
        dimens = set()
        vectors = []
        hot_blogs = []
        for blog in blogs:
            blog_info = blog[4]
            forward = blog[5]
            comment = blog[6]
            blog_thumbup = blog[7]
            val = math.sqrt(forward ** 2 + comment ** 2 + blog_thumbup ** 2)
            # full_blog_info += blog_info

            if val > 100:
                # print blog_info
                segs = jieba.analyse.textrank(blog_info, topK=1000, withWeight=True)
                dims = []
                datas = []
                v = []
                for dim,data in segs:
                    dimens.add(dim)

        for blog in blogs:
            blog_info = blog[4]
            forward = blog[5]
            comment = blog[6]
            blog_thumbup = blog[7]
            val = math.sqrt(forward ** 2 + comment ** 2 + blog_thumbup ** 2)
            # full_blog_info += blog_info

            if val > 100:
                hot_blogs.append(blog)
                print blog_info
                segs = jieba.analyse.textrank(blog_info, topK=1000, withWeight=True)
                dims = []
                datas = []
                v = []
                for dim,data in segs:
                    dims.append(dim)
                    datas.append(data)
                for dimen in dimens:
                    if dimen in dims:
                        v.append(datas[dims.index(dimen)])
                    else:
                        v.append(0)

                vectors.append(v)



        data = [array(v) for v in vectors]
        # print data
        ga = nltk.cluster.gaac.GAAClusterer(num_clusters = 5, normalise = True)
        ga.cluster(vectors=data)
        for i in range(len(hot_blogs)):
            print "分类结果:",ga.classify(data[i])," 原文：",hot_blogs[i][4]

