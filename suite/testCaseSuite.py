import os.path
import pprint
import time
import unittest

import ddt
import logging
import json
import setting
from caseAssemble import CaseAssemble
from case_utils.excelutils import *
import requests
import sendrequests
from newReport import new_report
from package.HTMLTestRunner import HTMLTestRunner
from case_utils.assertUtils import *
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] '
                           '- %(levelname)s: %(message)s', level=logging.INFO)
e = ExcelUtils("../case/API_CASE_INFO.xlsx")
t = e.assemble_info()
bean = CaseAssemble(t)
bean.cfg_case()
testData = bean.res
print(testData)


@ddt.ddt
class Runner(unittest.TestCase):
    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        pass

    @ddt.data(*testData)
    def test_info(self, casedata):  # write your api  method
        # method = casedata['method']
        # url = casedata['URL']
        # param = casedata['params']
        # headers = casedata['headers']

        send = sendrequests.SendRequests()
        r = send.sendRequests(self.s, casedata)

        if r.json():
            res =AssertUtils().assertJson(r, casedata['assertByresponse'])
            self.assertTrue(res,True)
        # r = requests.request(method=method, url=url, headers=headers, data=json.dumps(param))
        # logging.info(json.dumps(param,sort_keys=True,ensure_ascii=False,indent=2))
        # print('response',json.dumps(r.json(),sort_keys=True,indent=2,ensure_ascii=False))
        # print('-------------------------------------------------------------------------------------------------------------------------------------')
        # print('request',json.dumps(r.json(),sort_keys=True,indent=2,ensure_ascii=False))
        #
        # self.assertTrue(r.json()['msg'] == '成功')


if __name__ == '__main__':
    pass
    # print('run')
    # suite = unittest.TestSuite()
    # discover = unittest.defaultTestLoader.discover(setting.TEST_CASE, pattern='testCaseSuite.py')
    # for suite in discover:
    #
    #     for case in suite:
    #         suite.addTest(case)
    #
    # suite.addTest(suite)
    # now = time.strftime("%Y-%m-%d_%H_%M_%S")
    # filename = setting.TEST_REPORT + '/' + now + 'result.html'
    # print(filename)
    # fp = open(filename, 'wb')
    # runner = HTMLTestRunner(stream=fp, title='发布会系统接口自动化测试报告',
    #                         description='环境：windows 7 浏览器：chrome',
    #                         tester='Jason')
    # runner.run(suite)
    # fp.close()
    # report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
