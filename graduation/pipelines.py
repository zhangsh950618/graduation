# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb, logging
from .items import *


class GraduationPipeline(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def open_spider(self, spider):
        # 连接到数据库。
        try:
            self.connector = MySQLdb.connect(host="localhost", user="root", passwd="123", db="graduation",
                                             use_unicode=True, charset="utf8")
            self.cursor = self.connector.cursor()
            self.logger.info('Conneting to database successfully!')
        except MySQLdb.Error as e:
            self.logger.info('Failed to connect to mysql')

        # class CommentItem(scrapy.Item):
        #     # 评论id主键唯一
        #     comment_id = scrapy.Field()
        #     # 评论所对应的微博文章的id，作为外键
        #     blog_id = scrapy.Field()
        #     # 评论的内容
        #     comment_info = scrapy.Field()
        #     # 评论的点赞数量
        #     comment_thumbup = scrapy.Field()
        #     # 评论的时间
        #     comment_time = scrapy.Field()



        # 如果表不存在就建立新的表blog
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS blog (blog_id varchar(200) PRIMARY KEY ,keyword varchar(200) ,post_time datetime,author varchar(200),blog_info text,forward INT ,comment INT ,blog_thumbup INT );',
        )

        # 如果表不存在就建立新的表comment
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS comment (comment_id varchar(200) PRIMARY KEY ,blog_id varchar(200),FOREIGN KEY(blog_id) REFERENCES blog(blog_id),comment_time datetime,comment_info text,comment_thumbup INT);',
        )

        # 关闭外键约束
        self.cursor.execute(
            'SET FOREIGN_KEY_CHECKS=0;',
        )
        self.connector.commit()
        self.logger.info('Table check finished!')

    def process_item(self, item, spider):
        if isinstance(item, BlogItem):
            statement = "REPLACE INTO blog VALUES ( %s, %s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(statement, (
                item['blog_id'], item['keyword'], item['post_time'], item['author'], item['blog_info'],
                item['forward'], item['comment'], item['blog_thumbup']))
            self.connector.commit()
        elif isinstance(item, CommentItem):
            statement = "REPLACE INTO comment VALUES ( %s, %s,%s,%s,%s)"
            self.cursor.execute(statement, (
                item['comment_id'], item['blog_id'], item['comment_time'], item['comment_info'],
                item['comment_thumbup']))
            self.connector.commit()
        return item
