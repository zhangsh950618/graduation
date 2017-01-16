# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dao.blog_dao import *
import math
from matplotlib import pyplot



# 绘制数据的分布图形
def plot_data_scatter():
    # 数据准备
    blog_dao = BlogDao()
    forwards = blog_dao.search_col_blogs("forward")
    comments = blog_dao.search_col_blogs("comment")

    blog_thumbups = blog_dao.search_col_blogs("blog_thumbup")
    cols = blog_dao.search_all_blogs()
    cols = list(cols)
    cols.sort(
        lambda x, y: cmp(math.sqrt(x[5] ** 2 + x[6] ** 2 + x[7] ** 2), math.sqrt(y[5] ** 2 + y[6] ** 2 + y[7] ** 2)),reverse=True)
    for col in cols:
        print math.sqrt(col[5] ** 2 + col[6] ** 2 + col[7] ** 2), col[4]
    fre = []
    for col in cols:
        forward = col[5]
        comment = col[6]
        blog_thumbup = col[7]
        val = math.sqrt(forward ** 2 + comment ** 2 + blog_thumbup ** 2)
        fre.append(val)
    pyplot.hist(fre, 10)

    pyplot.xlabel('fre')
    pyplot.xlim(0.0, 400)
    pyplot.ylabel('Frequency')
    pyplot.title('Lenth Of Fake Urls')
    pyplot.show()


        # if val > 100:
        #     print col[2], val, col[4]
    print fre
    ax = plt.figure().add_subplot(111, projection='3d')
    # 基于ax变量绘制三维图
    # xs表示x方向的变量
    # ys表示y方向的变量
    # zs表示z方向的变量，这三个方向上的变量都可以用list的形式表示
    # m表示点的形式，o是圆形的点，^是三角形（marker)
    # c表示颜色（color for short）

    ax.scatter(forwards, comments, blog_thumbups, c='r')  # 点为红色三角形

    # 设置坐标轴
    ax.set_xlabel('forwards Label')
    ax.set_ylabel('comments Label')
    ax.set_zlabel('blog_thumbups Label')

    # 显示图像
    plt.show()
