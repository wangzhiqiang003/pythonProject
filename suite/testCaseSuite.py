import os.path
import pprint
import time
import unittest


import ddt
import logging
import json

import caseAssemble
import setting
from caseAssemble import CaseAssemble
from case_utils.excelutils import *
import requests
import sendrequests
from newReport import new_report
from package.HTMLTestRunner import HTMLTestRunner
from case_utils.assertUtils import *
import logging
import redisutils
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
e = ExcelUtils("../case/API_CASE_INFO.xlsx")
t = e.assemble_info()
bean = CaseAssemble(t)
# bean.cfg_case()   #将案例的组装放到具体的执行中去，以便精准的获取到上下文的参数
testData = t
r = None
response = {}
req = {}


@ddt.ddt
class Runner(unittest.TestCase):

    def setUp(self):
        self.s = requests.session()

    def tearDown(self):
        logging.info('案例执行完毕，参数打印如下: 请求参数')
        logging.info(json.dumps(req, indent=2, sort_keys=True, ensure_ascii=False))
        if self.r:
            if response:
                logging.info("响应参数")
                logging.info(json.dumps(response, indent=2, sort_keys=True, ensure_ascii=False))
                if self.r:
                    traceId = self.r.headers.setdefault('traceId', None)
                    logging.info(f"traceId:{traceId}")
            # 处理请求参数、响应参数中需要保存得变量到redis
        CaseAssemble.save_req_res(self.casedata['save_req_res'], req, self.r)

        delayTime = int(self.casedata['delayTime'])
        logging.info('延迟时间为{}'.format(delayTime))
        time.sleep(delayTime)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        redisutils.myredis.clean_redis
        logging.info('结束执行' + str(time.time()))

    @ddt.data(*testData['case'])
    def test_info(self, casedata):  # write your api  method
        logging.info('>*' * 45 + f'{casedata["caseSubjet"]}' + '<*' * 45)
        self.casedata = casedata
        self.preHandleReq(self.casedata)
        send = sendrequests.SendRequests()
        self.r = send.sendRequests(self.s, self.casedata)
        if self.r and self.r.isJson:
            if self.r.json():

                res = AssertUtils().assertJson(self.r.json(), casedata['assertByresponse'])
                self.assertTrue(res, True)

    def preHandleReq(self, casedata):
        bean.handle(casedata)


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
    #                         tester='wangzhiqing')
    # runner.run(suite)
    # fp.close()
    # report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
