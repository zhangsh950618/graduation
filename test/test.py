# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/zsh/PycharmProjects/graduation')
from segmentation import  jieba_segmentation

jie_seg = jieba_segmentation.JiebaSeg()
jie_seg.get_segmention_for_all_blogs()
print sys.path
