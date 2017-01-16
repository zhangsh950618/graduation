# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/zsh/PycharmProjects/graduation')
from segmentation import  jieba_segmentation
from datamining.datascatter import  *
jie_seg = jieba_segmentation.JiebaSeg()
# jie_seg.get_segmention_for_all_blogs()
# plot_data_scatter()
jie_seg.get_top_keywords()
