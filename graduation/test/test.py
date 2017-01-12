# -*- coding: utf-8 -*-
import re
import datetime


a = "赞[123]"
a_re = re.compile("赞.*")
print a_re.findall(a)
a = "今天"
if a == "今天":
    print "yes"
print ((datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M"))



a = u"评论[10]"
a_re = re.compile(u'^评论\[\d+\]$')
if a_re.match(a):
    print "yes"

print re.match(u'今天', u'今天 10:01')



