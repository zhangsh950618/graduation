# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
from ..items import *
import time
from datetime import datetime, timedelta


class WeiboForSomethingSpider(CrawlSpider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = ['http://weibo.cn/']

    def get_time(self, post_time):
        return datetime.strptime(post_time.decode('utf-8'), '%a, %d %b %Y %H:%M:%S %Z')

    def handle_time(self, now_time, post_time):
        if re.match(u'\d+分钟前', post_time):
            return now_time - timedelta(minutes=int(re.findall('\d+', post_time)[0]))
        elif re.match(u'今天', post_time):
            temp_time = re.findall('\d+', post_time)
            return datetime(
                year=now_time.date().year,
                month=now_time.date().month,
                day=now_time.date().day,
                hour=int(temp_time[0]),
                minute=int(temp_time[1])
            )
        else:
            temp_time = re.findall(r'\d+', post_time)
            # x-x-x x:x
            if int(temp_time[0]) > 12:
                return datetime(
                    year=int(temp_time[0]),
                    month=int(temp_time[1]),
                    day=int(temp_time[2]),
                    hour=int(temp_time[3]),
                    minute=int(temp_time[4])
                )
            # x月x日 x:x
            else:
                return datetime(
                    year=now_time.date().year,
                    month=int(temp_time[0]),
                    day=int(temp_time[1]),
                    hour=int(temp_time[2]),
                    minute=int(temp_time[3])
                )

    def start_requests(self):
        self.logger.info('start crawl for something ...')
        # keywords = self.settings.get("CRAWLED_WEIBO_KEYWORDS_LIST")
        keyword = u"美国大选"
        keyword_url = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E7%BE%8E%E5%9B%BD%E5%A4%A7%E9%80%89&page=1&vt=4'
        # self.logger.info(keyword_url)
        yield scrapy.Request(
            url=keyword_url,
            meta={'keyword': keyword},
            callback=self.parse_keyword
        )

    def parse_keyword(self, response):
        self.logger.info('parsekeyword..')
        soup = BeautifulSoup(response.body, "lxml")
        # self.logger.info(soup.prettify())

        bolg_re = re.compile('M_.*')  # 筛选blog的标签
        blogs = soup.find_all('div', {'class': 'c', 'id': bolg_re})
        keyword = response.meta['keyword']
        # self.logger.info(keyword)
        for blog in blogs:
            # self.logger.info(blog.prettify())

            # 微博的id
            # 如果是转发的微博会产生一个新的blog_id
            # 转发的微博是否需要抓取，和老师商量
            blog_id = blog['id']
            # self.logger.info(blog_id)

            # 微博的作者
            author_a = blog.find('a', {'class': 'nk'})
            author = author_a.get_text()
            # self.logger.info(author)

            # 找到微博内容的div
            blog_info_div = blog.find('span', {'class': 'ctt'})
            blog_info = blog_info_div.get_text()
            # self.logger.info(blog_info)



            # 处理转发的微博，用原来的id代替现在的id
            # 转发的id会产生一个新的


            find_number = re.compile("\d+")

            # 微博发布的时间
            post_time_span = blog.find('span', {'class': 'ct'})
            post_time_string = re.split(u'来自', post_time_span.get_text())[0].strip()
            # self.logger.info(post_time_span.get_text())
            # self.logger.info(post_time_string)
            post_time = str(
                self.handle_time(self.get_time(response.headers['date']), post_time_string))
            # self.logger.info(post_time_string)
            # now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # self.logger.info(type(post_time_string))

            # post_time默认是当前时间
            # post_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 如果时间是今天 xx月xx日
            # if post_time_date == u"今天":
            #     # 如果是今天，首先获取当前的日期
            #     # self.logger.info("今天")
            #     today = datetime.datetime.today()
            #     post_time_datetime = post_time_string[1]
            #     hour = int(post_time_datetime[0:2])
            #     min = int(post_time_datetime[3:5])
            #     post_time = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=hour, minute=min)
            #     # self.logger.info(post_time)
            #
            # # 如果时间是xx分钟前
            # elif post_time_date[-1] == u"前":
            #     min_pre = int(post_time_date[:-3])
            #     post_time = (datetime.datetime.now() - datetime.timedelta(minutes=min_pre)).strftime("%Y-%m-%d %H:%M")
            #     # self.logger.info(post_time)
            #
            # # 如果时间显示为xx月xx日的处理方法
            # elif post_time_date[-1] == u"日":
            #     year = 2017
            #     mon = int(post_time_date[0:2])
            #     day = int(post_time_date[3:5])
            #     post_time_datetime = post_time_string[1]
            #     hour = int(post_time_datetime[0:2])
            #     min = int(post_time_datetime[3:5])
            #     post_time = datetime.datetime(year=year, month=mon, day=day, hour=hour, minute=min)
            #     # self.logger.info(post_time)

            # 查找这个微博的关键字
            # self.logger.info(keyword)

            # “评论”

            comment_a = blog.find('a', text = re.compile(u'^评论\[\d+\]$'))
            # self.logger.info(comment_a)
            comment = int(find_number.search(comment_a.get_text()).group())
            # self.logger.info("评论数量为：{0}".format(comment))
            if comment != 0:
                # self.logger.info(comment_a)
                comment_url = comment_a['href']
                # self.logger.info(comment_url)
                yield scrapy.Request(
                    url=comment_a['href'],
                    meta={'blog_id': blog_id},
                    callback=self.parse_comment
                )

            # “转发”
            forward_a = blog.find('a', text = re.compile(u'^转发\[\d+\]$'))
            forward = int(find_number.search(forward_a.get_text()).group())
            # self.logger.info(forward_a)
            # self.logger.info("转发数量为：{0}".format(forward))

            # “点赞”
            blog_thumbup_a = blog.find('a', text = re.compile(u'^赞\[\d+\]$'))
            # self.logger.info(blog_thumbup_a)
            blog_thumbup = int(find_number.search(blog_thumbup_a.get_text()).group())
            # self.logger.info("点赞数量为：{0}".format(blog_thumbup))

            blog_item = BlogItem(
                # 博文id应该是唯一的
                blog_id=blog_id,
                # 所搜索微博文章的关键字
                keyword=keyword,
                # 博文的作者
                author=author,
                # 博文发布的时间
                post_time=post_time,
                # 博文的内容
                blog_info=blog_info,
                # 博文的转发量
                forward=forward,
                # 博文的评论数量
                comment=comment,
                # 博文的点赞数量
                blog_thumbup=blog_thumbup,
            )

            #  用于处理长文字，在当前页面下面显示不下了，存在“全文”的链接单独做处理
            # 只需要重新抓取blog_info字段就可以了
            full_text_a = blog.find('a', text="全文")

            # 如果存在全文链接
            if full_text_a is not None:
                full_text_href = full_text_a['href']
                full_text_url = 'http://weibo.cn' + full_text_href

                # 不返回item
                yield scrapy.Request(
                    url=full_text_url,
                    meta={'blog_item': blog_item},
                    callback=self.parse_full_text
                )
            else:
                yield blog_item
        next_page = soup.find("a", text="下页")
        # self.logger.info(next_page)
        if next_page is not None:
            href = next_page['href']
            # self.logger.info(href)
            next_url = 'http://weibo.cn' + href
            yield scrapy.Request(
                url=next_url,
                meta={'keyword': keyword},
                callback=self.parse_keyword
            )

    def parse_full_text(self, response):
        # 首先抓取原来的数据
        blog_item = response.meta['blog_item']
        soup = BeautifulSoup(response.body, "lxml")
        # 将blog_info替换成新的全文的full_text
        blog_item['blog_info'] = soup.find('span', {'class': 'ctt'}).get_text()

        yield blog_item

    def parse_comment(self, response):
        blog_id = response.meta['blog_id']
        soup = BeautifulSoup(response.body, "lxml")
        comments = soup.find_all('div', {'class': 'c', "id": re.compile("^C_.*")})

        # self.logger.info(soup.prettify())

        # # 评论id主键唯一
        # comment_id = scrapy.Field()
        # # 评论所对应的微博文章的id，作为外键
        # blog_id = scrapy.Field()
        # # 评论的内容
        # comment_info = scrapy.Field()
        # # 评论的点赞数量
        # comment_thumbup = scrapy.Field()
        # # 评论的时间



        for comment in comments:
            comment_id = comment['id']
            # self.logger.info(comment.prettify())
            comment_info_span = comment.find('span', {'class': 'ctt'})
            # self.logger.info(comment_info_span.contents)
            # 如果这条评论是回复的别人的，跳过
            if comment_info_span.contents[0] == u"回复":
                # self.logger.info("回复")
                continue
            comment_info = comment_info_span.get_text()
            find_number = re.compile("\d+")
            # “点赞”
            comment_thumbup_a = comment.find('a', text=re.compile(u'^赞\[\d+\]$'))
            # self.logger.info(blog_thumbup_a)
            comment_thumbup = int(find_number.search(comment_thumbup_a.get_text()).group())
            # self.logger.info("点赞数量为：{0}".format(comment_thumbup))

            # 微博发布的时间
            comment_time_span = comment.find('span', {'class': 'ct'})
            # comment_time_string = comment_time_span.get_text().split()
            # comment_time_date = comment_time_string[0]

            comment_time_string = re.split(u'来自', comment_time_span.get_text())[0].strip()
            # self.logger.info(post_time_span.get_text())
            # self.logger.info(post_time_string)
            comment_time = str(
                self.handle_time(self.get_time(response.headers['date']), comment_time_string))

            # self.logger.info(post_time_string)
            # now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # self.logger.info(type(post_time_string))

            # post_time默认是当前时间
            # comment_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 如果时间是今天 xx月xx日
            # if comment_time_date == u"今天":
            #     # 如果是今天，首先获取当前的日期
            #     # self.logger.info("今天")
            #     today = datetime.datetime.today()
            #     comment_time_datetime = comment_time_string[1]
            #     hour = int(comment_time_datetime[0:2])
            #     min = int(comment_time_datetime[3:5])
            #     post_time = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=hour, minute=min)
            #     # self.logger.info(post_time)
            #
            # # 如果时间是xx分钟前
            # elif comment_time_date[-1] == u"前":
            #     min_pre = int(comment_time_date[:-3])
            #     comment_time = (datetime.datetime.now() - datetime.timedelta(minutes=min_pre)).strftime("%Y-%m-%d %H:%M")
            #     # self.logger.info(comment_time)
            #
            # # 如果时间显示为xx月xx日的处理方法
            # elif comment_time_date[-1] == u"日":
            #     year = 2017
            #     mon = int(comment_time_date[0:2])
            #     day = int(comment_time_date[3:5])
            #     post_time_datetime = comment_time_string[1]
            #     hour = int(comment_time_date[0:2])
            #     min = int(comment_time_date[3:5])
            #     comment_time = datetime.datetime(year=year, month=mon, day=day, hour=hour, minute=min)
            #     # self.logger.info(comment_time)

            comment_item = CommentItem(
                # 博文id应该是唯一的
                comment_id=comment_id,
                # 所搜索微博文章的关键字
                blog_id=blog_id,
                # 博文的作者
                comment_info=comment_info,
                # 博文发布的时间
                comment_thumbup=comment_thumbup,
                # 博文的内容
                comment_time=comment_time,
            )
            yield comment_item

        next_page = soup.find("a", text="下页")
        # self.logger.info(next_page)
        if next_page is not None:
            href = next_page['href']
            # self.logger.info(href)
            page = int(href.split("=")[-1])
            if page < 15:
                next_url = 'http://weibo.cn' + href
                yield scrapy.Request(
                    url=next_url,
                    meta={'blog_id': blog_id},
                    callback=self.parse_comment
                )
