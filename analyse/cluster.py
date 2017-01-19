# -*- coding: utf-8 -*-

import math
from jieba_segmentation import JiebaSeg
import numpy as np
from entity.blog_entity import *


def get_dimens(blogs):
    dimens = set()
    jieba_seg = JiebaSeg()
    for blog in blogs:
        blog_info = blog[4]
        segs = jieba_seg.get_segmention_for_blog(blog_info)
        for seg, weight in segs:
            dimens.add(seg)
    return dimens


# 将关键词的权重转换成向量
# dimens表示全局的维度
# segs是一个元组列表[(单词，权重)...]

# 对于稀疏向量做泛化处理
def normalize(segs):
    sum = 0
    for seg,weight in segs:
        sum += weight ** 2
    norm = math.sqrt(sum)
    for i in range(len(segs)):
        segs[i] = list(segs[i])
        segs[i][1] /= norm



def gaac(keyword):
    jieba_seg = JiebaSeg()
    # 筛选热度高于100的节点作为热点
    hot_blogs = jieba_seg.get_hot_blogs(keyword, 65)

    # 首先获取所有的单词维度
    # dimens = get_dimens(hot_blogs)
    # print dimens
    # segmentions返回的是元组列表
    # [(单词1，权重1),(单词2，权重2)...]
    # 将vector作为特征向量
    hot_blog_entities = []
    for hot_blog in hot_blogs:
        # get_vector 方法将所有的segmentions返回的是元组转换成向量，词组如果存在就是weight不存在就是0
        segs = jieba_seg.get_segmention_for_blog(hot_blog[4])
        normalize(segs)
        hot_blog_entities.append(
            [BlogEntity(segs, hot_blog)])

    # 现在已经将所有的数据封装到hot_blog_entities中了
    # 开始聚类
    flag = False
    while flag is not True:
        # 总的实体的个数
        tot_entities = len(hot_blog_entities)
        # 寻找最近的两类合并
        v = 0
        t = 0
        max_similarity = 0
        for i in range(tot_entities):
            for j in range(i + 1, tot_entities):
                similarity = get_similarity(hot_blog_entities[i], hot_blog_entities[j])
                if similarity > max_similarity:
                    max_similarity = similarity
                    v = i
                    t = j
        print max_similarity
        if max_similarity < 0.5:
            flag = True
        # 将hot_blog_entities中 index 为v和t的合并
        else:
            merge(hot_blog_entities, v, t)
            tot_entities -= 1



    #聚类结束
    i = 0
    for entity in hot_blog_entities:
        if len(entity) > 2:
            print i
            i += 1
            for blog in entity:
                print blog.get_blog_info()


def get_distance(v1,v2):
    sum = 0
    for seg1,weight1 in v1:
        for seg2,weight2 in v2:
            if seg1 == seg2:
                sum += weight1 * weight2
    return sum


def get_similarity(blog_entity1, blog_entity2):
    dot_products = []
    for e1 in blog_entity1:
        for e2 in blog_entity2:
            v1 = e1.get_vector()
            v2 = e2.get_vector()
            dot_products.append(get_distance(v1,v2))
    # 返回的是中位数，也可以尝试平均数
    dot_products.sort()
    length = len(dot_products)
    return dot_products[length / 2]

    # 使用平均值，貌似还是中位数比较靠谱
    # return sum(dot_products)/len(dot_products)


def merge(blog_entities, v, t):
    blog_entities[v].extend(blog_entities[t])
    blog_entities.pop(t)
