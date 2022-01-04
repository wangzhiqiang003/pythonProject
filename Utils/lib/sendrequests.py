#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'wangzhiqaing'

import logging
import os, sys, json
import re
import string
import time
import urllib

import requests
import requests_cache

import testCaseSuite

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='myapp.log',
                # filemode='w'
                    )
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class SendRequests():
    """发送请求数据"""

    def sendRequests(self, s, apiData):
        headers = apiData['headers']

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

                elif headers['Content-Type'] in 'application/json;charset=UTF-8':
                    body = json.dumps(par)
                    par = None
            elif method == 'get':
                par = urllib.parse.urlencode(par)
                body = None

            testCaseSuite.req = apiData['params']
            allow_redirects = True

            user_allow_redirect = apiData['allow_redirects']
            allow_redirects = False if user_allow_redirect == 'N' else True

            # 发送请求
            logging.info(f"url is: {url}")
            r: requests.models.Response = s.request(method=method, url=url, headers=h, params=par, data=body,
                                                    verify=False, allow_redirects=allow_redirects)
            r.isJson = self.isJson(r)

            locations = r.headers.setdefault('Location', None)
            logging.info(locations)

            if 200 <= r.status_code < 400:
                cookie = s.cookies.items()
                if cookie:
                    cookie = cookie[0]
                    r.headers.update({"Cookie": "=".join(cookie)})
                print('request', json.dumps(apiData['params'], ensure_ascii=False, indent=2))
                content_type: str = r.headers.setdefault('Content-Type', 'text/html;charset=UTF-8')
                logging.info(json.dumps(apiData['headers'], ensure_ascii=False, indent=2))
                isJson = True
                logging.info(r.headers)
                if content_type.lower() in 'text/html;charset=UTF-8'.lower():
                    testCaseSuite.response = r.text
                    print(testCaseSuite.response)
                    logging.info(testCaseSuite.response)
                    logging.info(r.headers)
                    traceId = r.headers.setdefault('traceId', None)
                    print("traceId: ", traceId)
                    logging.info(f"traceId:{traceId}")


                else:
                    print('-' * 124)
                    logging.info(f'json请求响应码{r.status_code}')
                    print('response', json.dumps(r.json(), ensure_ascii=False, indent=2))
                    # logging.info(json.dumps(r.headers, ensure_ascii=False, indent=2))
                    print('response', r)
                    traceId = r.headers.setdefault('traceId', None)
                    print(traceId)

                    testCaseSuite.response = r.json()


                # 处理重定向
                if locations and 300 <= r.status_code < 400:
                    h['Cookie'] = "=".join(cookie)
                    r: requests.models.Response = s.request(method=method, url=locations, headers=h, params=par,
                                                            data=body,
                                                            verify=False, allow_redirects=allow_redirects)
                    r.isJson = self.isJson(r)
                    if 300 < r.status_code < 400:  # 风险审批系统专用
                        locations = r.headers['Location']
                        logging.info(locations)
                        if locations:
                            patter = r'.*#access_token=(?P<access_token>(.*?))&token_type=(?P<token_type>(.*?))&.*'
                            resgroup = re.match(patter, locations)
                            if resgroup:
                                access_token = resgroup.groupdict().setdefault('access_token', '')
                                token_type = resgroup.groupdict().setdefault('token_type', '')
                                token_info = f'{token_type} {access_token}'
                                r.headers['Authorization'] = token_info
                                r.isJson = self.isJson(r)
                                print(r.text)
                                logging.info(f'响应参数为{r.text}')
                                traceId = r.headers.setdefault('traceId', None)
                                print(traceId)

                return r
            else:
                logging.info(r.text)
                return None
        except Exception as e:
            logging.error(f'请求方式异常{e}')
            print(e)

    def isJson(self, r):
        try:
            json.dumps(r.json(), indent=2, ensure_ascii=False)
            return  True
        except Exception as e :
            return False
