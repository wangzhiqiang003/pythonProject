#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'YinJia'

import os


def new_report(testreport):
    """
    生成最新的测试报告文件
    :param testreport:
    :return:返回文件
    """
    lists = os.listdir(testreport)
    # 将存量的报告删除,只留最新的
    if len(lists) > 1:
        for file in lists[0:-2]:
            tempfile = os.path.join(testreport, file)
            if os.path.isfile(tempfile):
                os.remove(tempfile)
    lists = os.listdir(testreport)
    # lists.sort(key=lambda fn: os.path.getmtime(testreport + "\\" + fn))
    file_new = os.path.join(testreport, list(filter(lambda x: os.path.isfile(os.path.join(testreport, x)), lists))[0])
    print(file_new)
    return file_new
