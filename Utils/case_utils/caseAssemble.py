import json
import re
import jsonpath
import addict
import re
import importlib
import globalData

myDataUtils = importlib.import_module('Utils.base_data_utils.DataUtils', '.')
from operator import methodcaller


class CaseAssemble:
    def __init__(self, caseInfoList):
        self.caselist = caseInfoList['case']
        self.envList = caseInfoList['env']
        self.apiList = caseInfoList['api']
        self.res = []

    def get_api_by_apiId(self, api_id):
        return list(filter(lambda x: x['apiId'] == api_id, self.apiList))[0]

    def get_env_by_envId(self, envId):
        pass

    def get_case_by_caseId(self, caseId):
        pass

    def get_envId_from_case_info(self):
        pass

    def get_apiId_from_case_info(self, item):
        return item['apiId']

    def getApiInfo(self, item):
        apiId = self.get_apiId_from_case_info(item)
        apiInfo = self.get_api_by_apiId(apiId)
        item['method'] = apiInfo['method']

        return apiInfo

    def sign_data(self, item):
        param = item['params']
        apiInfo = self.getApiInfo(item)
        new_dict = addict.Dict(apiInfo)
        user_strategy = apiInfo['signature_strategy']
        signature_strategylist = user_strategy.split(',') if user_strategy else {}

        signature_strategylist = list(map(lambda x: 'new_dict' + x[1:], signature_strategylist))
        signature_strategylist = list(map(lambda x: re.sub(r'\$', '', x), signature_strategylist))
        for x in signature_strategylist:
            key, value = x.split("=")
            res = re.findall(r'\{__(.*)\(\)?\}.*', value)
            if res:
                fun = res[0]
                obj = getattr(myDataUtils, 'DataUtils')()
                md = getattr(obj, fun)
                value = md(item['params'])  # 这里调用方法，可以传入参数
                new_dict = addict.Dict(item['headers'])
                new_dict[key.split('.')[1]] = value
                item['headers'] = new_dict
                globalData.globalsData[key.split('.')[-1]] = value
    def addHeader(self, item):
        apiInfo = self.getApiInfo(item)
        orginHeader =apiInfo['defaultHeader']
        orginHeader = orginHeader if orginHeader else '{}'
        tempparam = eval(orginHeader)

        user_header = item['headers']
        if user_header:
            new_dict = addict.Dict(tempparam)
            list_param = user_header.split(',') if user_header else {}
            list_param = list(map(lambda x: 'new_dict' + x[1:], list_param))
            list_param = list(map(lambda x: re.sub(r'\$', '', x), list_param))
            for x in list_param:
                key, value = x.split("=")

                res = re.findall(r'\{__(.*)\(\)?\}.*', value)
                if res:

                    fun = res[0]

                    # value = methodcaller(fun)(DataUtils)
                    obj = getattr(myDataUtils, 'DataUtils')()
                    md = getattr(obj, fun)
                    value = md()  # 这里调用方法，可以传入参数
                    globalData.globalsData[key.split('.')[-1]] = value

                else:
                    pass

                x = '='.join((str(key), value))
                exec(x)
            item['headers'] = new_dict
        else:
            item['headers'] = tempparam

    def handle(self, item):

        self.addHeader(item)
        self.addParam(item)
        self.addUrl(item)
        self.sign_data(item)
        self.res.append(item)

    def addParam(self, item):
        apiInfo = self.getApiInfo(item)

        orginParam =apiInfo['defualt_param']
        orginParam = orginParam if orginParam else '{}'
        tempparam = eval(orginParam)
        user_param = item['params']
        if user_param:
            new_dict = addict.Dict(tempparam)
            list_param = user_param.split(',') if user_param else {}
            list_param = list(map(lambda x: 'new_dict' + x[1:], list_param))
            list_param = list(map(lambda x: re.sub(r'\$', '', x), list_param))
            for x in list_param:
                key, value = x.split('=')

                # 从字典中去找对应的变量进行替换  '${#customerName}'
                resdict = re.findall(r'\{#(.*)\}', value)
                if resdict:
                    value = globalData.globalsData[resdict[0]]
                    x = '='.join((str(key), repr(value)))
                    exec(x)
                res = re.findall(r'\{__(.*)\(\)?\}.*', value)

                # 调用随机数据生成函数来替换变量
                if res:
                    fun = res[0]

                    obj = getattr(myDataUtils, 'DataUtils')()
                    md = getattr(obj, fun)
                    value = md()  # 这里调用方法，可以传入参数
                    x = '='.join((str(key), repr(value)))
                    globalData.globalsData[key.split('.')[-1]] = value

                exec(x)
            item['params'] = new_dict
        else:
            item['params'] = tempparam

    def cfg_case(self):
        for item in self.caselist:
            self.handle(item)

    def addUrl(self, item):
        apiInfo = self.getApiInfo(item)
        baseUrl = self.getEnv(item)
        all_url = baseUrl + apiInfo['url']
        item['URL'] = all_url

    def getEnv(self, item):
        envId = item['envId']
        envInfo = list(filter(lambda x: x['envId'] == envId, self.envList))[0]
        return envInfo['host']
