#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = '王智强'

from newReport import new_report
from config import setting
from time import *
from package.HTMLTestRunner import *
import unittest
from suite import *


def add_case(test_path=setting.TEST_CASE):
    test_suite = unittest.TestSuite()

    """加载所有的测试用例"""
    discover = unittest.defaultTestLoader.discover(test_path, pattern='testCaseSuite.py')
    for suite in discover:
        for case in suite:
            test_suite.addTest(case)
    return test_suite


def run_case(all_case, result_path=setting.TEST_REPORT):
    """执行所有的测试用例"""

    # 初始化接口测试数据
    # test_data.init_data()

    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    filename = result_path + '/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='runthink接口自动化测试报告',
                            description='环境：windows 7 浏览器：chrome',
                            tester='wangzhiqiang')
    runner.run(all_case)
    fp.close()
    report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    # send_mail(report)  # 调用发送邮件模块


if __name__ == "__main__":
    cases = add_case()
    run_case(cases)
