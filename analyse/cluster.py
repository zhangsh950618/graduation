# -*- coding: utf-8 -*-

import math
from jieba_segmentation import JiebaSeg
import numpy as np
from entity.blog_entity import *
from dao.blog_dao import *
import sys


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
    for seg, weight in segs:
        sum += weight ** 2
    norm = math.sqrt(sum)
    for i in range(len(segs)):
        segs[i] = list(segs[i])
        segs[i][1] /= norm


def gaac_for_hotblogs(keyword, hot, min_similarity):
    jieba_seg = JiebaSeg()
    # 筛选热度高于100的节点作为热点
    hot_blogs = jieba_seg.get_hot_blogs(keyword, hot)

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
        #     segmentions = ""
        #     for seg, weight in segs:
        #         segmentions += "," + seg
        #     print segmentions

        normalize(segs)
        hot_blog_entities.append(
            [BlogEntity(segs, hot_blog)])

    # 现在已经将所有的数据封装到hot_blog_entities中了
    # 开始聚类
    flag = False
    while flag is not True:
        # 总的实体的个数
        tot_entities = len(hot_blog_entities)
        print tot_entities
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
        if max_similarity < min_similarity:
            flag = True
        # 将hot_blog_entities中 index 为v和t的合并
        else:
            merge(hot_blog_entities, v, t)

    # 聚类结束
    i = 0
    for entity in hot_blog_entities:
        if len(entity) > 2:
            print i
            i += 1
            for blog in entity:
                print blog.get_blog_info()

    return hot_blog_entities


def get_distance(v1, v2):
    sum = 0
    for seg1, weight1 in v1:
        for seg2, weight2 in v2:
            if seg1 == seg2:
                sum += weight1 * weight2
    return sum


def get_similarity(blog_entity1, blog_entity2):
    # print  blog_entity1
    dot_products = []
    for e1 in blog_entity1:
        for e2 in blog_entity2:
            v1 = e1.get_vector()
            v2 = e2.get_vector()
            dot_products.append(get_distance(v1, v2))
    # 返回的是中位数，也可以尝试平均数
    dot_products.sort()
    length = len(dot_products)
    return dot_products[length / 2]

    # 使用平均值，貌似还是中位数比较靠谱
    # return sum(dot_products)/len(dot_products)


def merge(blog_entities, v, t):
    blog_entities[v].extend(blog_entities[t])
    blog_entities.pop(t)


def k_means_for_allblogs(hot_blog_entities, keyword, min_similarity):
    blog_dao = BlogDao()
    blogs = blog_dao.search_all_blogs(keyword)
    jieba_seg = JiebaSeg()
    blog_entities = []
    for blog in blogs:
        segs = jieba_seg.get_segmention_for_blog(blog[4])
        # normalize
        normalize(segs)
        blog_entities.append(
            BlogEntity(segs, blog))
    classified_blog_entities = hot_blog_entities
    tot_blogs = len(blog_entities)
    tot_entities = len(classified_blog_entities)
    for i in range(tot_blogs):
        print "the", i, "blog"
        max_similarity = 0
        t = 0
        for j in range(tot_entities):
            # temp_list = []
            # temp_list.append()
            similarity = get_similarity([blog_entities[i]], classified_blog_entities[j])
            if similarity > max_similarity:
                max_similarity = similarity
                t = j

        if max_similarity > min_similarity:
            classified_blog_entities[t].append(blog_entities[i])
    return classified_blog_entities


def get_classfied_blogs(keyword, hot, min_similarity, min_quantity):
    f_name = str(keyword[0]) + "_" + str(hot) + "_" + str(min_similarity) + "_" + str(min_quantity) + ".txt"
    f = open(f_name, 'w')

    # 对高热度blog进行层次聚类
    hot_blog_entities = gaac_for_hotblogs(keyword, hot, min_similarity)
    print "after gaac:", len(hot_blog_entities)
    f.write("层次聚类结果: 一共 " + str(len(hot_blog_entities)) + "\n")

    classified_blogs = k_means_for_allblogs(hot_blog_entities, keyword, min_similarity)
    print "after classified_blogs:", len(classified_blogs)

    tot_entities = len(classified_blogs)

    f.write("一共聚出:" + str(tot_entities) + "\n")
    l = 0
    for i in range(tot_entities):
        if len(classified_blogs[i]) > min_quantity:
            f.write(str(i) + '\n')
            l += 1
    f.write("核心类:" + str(l) + "\n")

    for i in range(tot_entities):
        if len(classified_blogs[i]) > min_quantity:
            f.write(str(i) + '\n')
            for blog in hot_blog_entities[i]:
                # print blog.get_blog_info()
                f.write(str(blog.get_blog_info()) + '\n')

    f.close()

    return classified_blogs, hot_blog_entities
