# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('/home/zsh/PycharmProjects/graduation')
from analyse import cluster


# cluster.get_classfied_blogs(["郑爽", "Yeah虚拟小号"], 100, 0.8, 30)
cluster.get_classfied_blogs(["郑爽", "Yeah虚拟小号"], 0, 0.8, 30)
