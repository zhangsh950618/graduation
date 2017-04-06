# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('/home/zsh/PycharmProjects/graduation')
from analyse import cluster
from analyse import sentiment

# cluster.get_classfied_blogs(["郑爽", "Yeah虚拟小号"], 100, 0.8, 30)
for s in range(30, 100,):
    for m in range(5, 50):
        cluster.get_classfied_blogs(["Yeah虚拟小号","郑爽"], 0, float(s)/100, m)
