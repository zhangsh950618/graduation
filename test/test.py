# -*- coding: utf-8 -*-
import sys
from dao.comment_dao import *
from analyse.sentiment import *
import numpy as np
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('/home/zsh/PycharmProjects/graduation')
from analyse import cluster
from analyse import sentiment

all_blog_entities = cluster.get_classfied_blogs(["郑爽", "Yeah虚拟小号"], 2500, 0.5, 12)

# data = []
# for blog_entity in all_blog_entities:
#     data.append(max(blog_entity, key=lambda obj: obj.get_hot_point()))
#
# data.sort(key=lambda obj: obj.get_post_time())
# c_dao = CommentDao()
# senti = Sentiment()
# for d in data:
#
#     comments = c_dao.search_all_comments_with_ids([d.get_blog_id()])
#     score = 0
#     for comment in comments:
#         score += senti.single_review_sentiment_score(comment[3])
#     # score /= len(comments)
#     print d.get_hot_point(), d.get_post_time(), d.get_blog_info(), score
c_dao = CommentDao()
senti = Sentiment()
all_blog_entities.sort(key=lambda obj: max(obj, key=lambda ob: ob.get_hot_point()).get_post_time())
scores = []
data = []
for blog_entity in all_blog_entities:
    blog_ids = []
    for blog in blog_entity:
        blog_ids.append(blog.get_blog_id())
    comments = c_dao.search_all_comments_with_ids(blog_ids)
    score = 0
    for comment in comments:
        score += senti.single_review_sentiment_score(comment[3])
    most_hot_blog = max(blog_entity,  key=lambda obj: obj.get_hot_point())
    # score /= len(comments)
    scores.append(score)

scores = np.array(scores)

scores = (scores)/(scores.max() - scores.min())

for index, blog_entity in enumerate(all_blog_entities):
    most_hot_blog = max(blog_entity, key=lambda obj: obj.get_hot_point())
    print most_hot_blog.get_post_time(), most_hot_blog.get_blog_info(), scores[index]
    data.append((most_hot_blog, scores[index]))




