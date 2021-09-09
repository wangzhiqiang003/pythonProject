#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'YinJia'

import logging
import os, sys, json
import urllib

logging.basicConfig(level=logging.INFO)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class SendRequests():
    """发送请求数据"""

    def sendRequests(self, s, apiData):

        # method = casedata['method']
        # url = casedata['URL']
        # param = casedata['params']
        # headers = casedata['headers']
        headers = apiData['headers']
        logging.info(headers)

        logging.info(apiData['params'])
        try:
            # 从读取的表格中获取响应的参数作为传递
            method = apiData["method"]
            url = apiData["URL"]
            if apiData["params"] == "":
                par = None
            else:
                par = apiData["params"]
            if apiData["headers"] == "":
                h = None
            else:
                h = apiData["headers"]
            if method == 'post':

                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    body = urllib.parse.urlencode(par)
                    logging.info(body)
                elif headers['Content-Type'] == 'application/json;charset=UTF-8':
                    body = json.dumps(par)
                    par = None
            elif method == 'get':
                par = urllib.parse.urlencode(par)
                logging.info(url + par)


            # 发送请求
            logging.info('start')
            r = s.request(method=method, url=url, headers=h, params=par, data=body, verify=False)
            logging.info('r.url')
            logging.info(str(r))
            print('request', json.dumps(apiData['params'], ensure_ascii=False, indent=2))
            print(
                '-------------------------------------------------------------------------------------------------------------------------------------')
            print('request', json.dumps(r.json(), ensure_ascii=False, indent=2))

            logging.info(r.json())
            return r
        except Exception as e:
            print(e)
