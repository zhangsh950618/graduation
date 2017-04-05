# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    # 博文id应该是唯一的
    blog_id = scrapy.Field()
    # 所搜索微博文章的关键字
    keyword = scrapy.Field()
    # 博文的作者
    author = scrapy.Field()
    # 博文发布的时间
    post_time = scrapy.Field()
    # 博文的内容
    blog_info = scrapy.Field()
    # 博文的转发量
    forward = scrapy.Field()
    # 博文的评论数量
    comment = scrapy.Field()
    # 博文的点赞数量
    blog_thumbup = scrapy.Field()


class CommentItem(scrapy.Item):
    # 评论id主键唯一
    comment_id = scrapy.Field()
    # 评论所对应的微博文章的id，作为外键
    blog_id = scrapy.Field()
    # 评论的内容
    comment_info = scrapy.Field()
    # 评论的点赞数量
    comment_thumbup = scrapy.Field()
    # 评论的时间
    comment_time = scrapy.Field()
