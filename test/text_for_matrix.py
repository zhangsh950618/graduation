# -*- coding: utf-8 -*-

from analyse import sentiment
from dao import comment_dao
import re
from matplotlib import pyplot as plt
import numpy as np
import math
s = sentiment.Sentiment()

com_dao = comment_dao.CommentDao()

comments = com_dao.search_all_comments_with_limit(1000)
scores = []
f = open('res.txt', 'w')
for comment in comments:
    raw_comment_info = comment[3].encode('utf-8')
    comment_info = re.sub('(@\S*|\[.*\]|#.*#|秒拍视频|转发微博)', "", raw_comment_info)
    val = s.single_review_sentiment_score(comment_info)
    scores.append(val)
    f.write("得分:" + str(val) + "\n")
    f.write("原始:" + raw_comment_info + "\n")
    f.write("处理后:" + comment_info + "\n")
    f.write("\n")
f.close()
print "max = " + str(max(scores)), "min = " + str(min(scores))
data = np.array(scores)
data = (data - data.mean()) / (data.max() - data.min())
bins = np.linspace(-1, 1, 20)
plt.hist(data, bins=bins)
plt.show()

