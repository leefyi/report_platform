#!/usr/local/bin python
# coding=utf-8
# @Time    : 2018/8/8 下午10:38
# @Author  : lifangyi
# @File    : echarts.py
# @Software: PyCharm

from pyecharts import Bar, Line, Pie, ThemeRiver
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


def generate_bar(names, values, width=550, height=350, *args, **kwargs):
    bar = Bar(
        title='今日测试总览',
        subtitle='用例运行结果柱状分布',
        width=width,
        height=height)
    case = names
    result = values
    total = values[0]
    bar.use_theme(theme_name='infographic')
    bar.add(
        '用例',
        case,
        result,
        is_label_show=True,
        is_visualmap=True,
        visual_range=[
            0,
            total])
    bar.render(TEMPLATE_DIR + '/bar.html')


def generate_line(attr, v, width=500, height=350, *args, **kwargs):
    line = Line('用例失败趋势图', width=width, height=height)
    line.add('失败统计', attr, v, is_smooth=False, mark_line=['max', 'average'])
    line.render(TEMPLATE_DIR + '/line.html')


def generate_timecost_line(attr, v, width=500, height=350, *args, **kwargs):
    line = Line('', width=width, height=height)
    line.add('耗时趋势', attr, v, is_smooth=False, mark_line=['average'])
    line.render(TEMPLATE_DIR + '/cost_line.html')


def generate_pie(attr, v, radius=[50, 50], *args, **kwargs):
    pie = Pie('今日用例情况-饼状图', title_pos='center')
    pie.add(
        '',
        attr,
        v,
        radius,
        label_text_color=None,
        is_label_show=True,
        legend_orient='virtical',
        legend_pos='left')
    pie.render(TEMPLATE_DIR + '/pie.html')


def generate_river(name, data, *args, **kwargs):
    river = ThemeRiver('平台分类-主题河流图')
    river.add(name, data, is_label_show=True)
    river.render(TEMPLATE_DIR + '/river.html')
