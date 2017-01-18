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
def get_vector(dimens, segs):
    vector = []
    # 计算
    sum = 0
    for dimen in dimens:
        flag = False
        for seg, weight in segs:
            if dimen == seg:
                flag = True
                vector.append(weight)
                sum += weight ** 2
        if flag is False:
            vector.append(0)
    # 将平方和开方得到范数
    norm = math.sqrt(sum)
    for i in range(len(vector)):
        vector[i] /= norm
    # 检验是否正确
    sum = 0
    for v in vector:
        sum += v ** 2
    print sum

    # 返回numpy的向量形式等下做dot运算
    return np.array(vector)


def gaac(keyword):
    jieba_seg = JiebaSeg()
    # 筛选热度高于100的节点作为热点
    hot_blogs = jieba_seg.get_hot_blogs(keyword, 50)

    # 首先获取所有的单词维度
    dimens = get_dimens(hot_blogs)
    print dimens
    # segmentions返回的是元组列表
    # [(单词1，权重1),(单词2，权重2)...]
    # 将vector作为特征向量
    hot_blog_entities = []
    for hot_blog in hot_blogs:
        # get_vector 方法将所有的segmentions返回的是元组转换成向量，词组如果存在就是weight不存在就是0
        hot_blog_entities.append(
            [BlogEntity(get_vector(dimens, jieba_seg.get_segmention_for_blog(hot_blog[4])), hot_blog)])

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
        if max_similarity < 0.3:
            flag = True
        # 将hot_blog_entities中 index 为v和t的合并
        else:
            merge(hot_blog_entities, v, t)
            tot_entities -= 1



    #聚类结束
    i = 0
    for entity in hot_blog_entities:
        print i
        i += 1
        for blog in entity:
            print blog.get_blog_info()


def get_similarity(blog_entity1, blog_entity2):
    dot_products = []
    for e1 in blog_entity1:
        for e2 in blog_entity2:
            v1 = e1.get_vector()
            v2 = e2.get_vector()
            dot_products.append(np.vdot(v1, v2))
    # 返回的是中位数，也可以尝试平均数
    dot_products.sort()
    length = len(dot_products)
    return dot_products[length / 2]


def merge(blog_entities, v, t):
    blog_entities[v].extend(blog_entities[t])
    blog_entities.pop(t)
