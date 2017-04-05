# -*- coding: utf-8 -*-
from dao.blog_dao import *

from util import connection


L = [1,2,3,4,5,6,1,1,1]

print L
for index,l in enumerate(L):
    if l == 1:
        L.pop(index)
print L