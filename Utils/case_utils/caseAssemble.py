import json
import logging
import re
import jsonpath
import addict
import re
import importlib
import redisutils
import dbutils
import globalData

myDataUtils = importlib.import_module('Utils.base_data_utils.DataUtils', '.')
from operator import methodcaller

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='myapp.log',
                # filemode='w'
                    )
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
                kw = key.split('.')[-1]
                globalData.globalsData[kw] = value
                a = {kw: value}

                redisutils.myredis.hmset('params', a)

    def addHeader(self, item):
        apiInfo = self.getApiInfo(item)
        orginHeader = apiInfo['defaultHeader']
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
                # 从字典中去找对应的变量进行替换  '${#customerName}'
                if 'issuedBy' in key:
                    print('issuedByissuedByissuedByissuedBy')
                resdict = re.search(r".*(\{#(.*)\})", value)

                if resdict:

                    kw = resdict.group(1)
                    kw1 = resdict.group(2)
                    logging.info(f'当前替换的字段为{kw}')
                    valuefromredis = redisutils.myredis.hmget('params', kw1)
                    valuefromredis=valuefromredis if valuefromredis else  ""
                    if type(value) == str:
                        value = re.sub(r'{}'.format(kw), valuefromredis, value)
                    x = '='.join((str(key), value))

                    try:
                        exec(x)
                    except Exception as e:
                        logging.info(e)

                res = re.findall(r'\{__(.*)\(\)?\}.*', value)
                if res:

                    fun = res[0]

                    # value = methodcaller(fun)(DataUtils)
                    obj = getattr(myDataUtils, 'DataUtils')()
                    md = getattr(obj, fun)
                    value = md()  # 这里调用方法，可以传入参数
                    kw = key.split('.')[-1]
                    # globalData.globalsData[kw] = value
                    redisutils.myredis.hmset('param', value)

                else:
                    pass

                x = '='.join((str(key), value))

                exec(x)
            item['headers'] = new_dict
            logging.info(f'items{item}')
        else:
            item['headers'] = tempparam

    def handle(self, item):

        self.addHeader(item)
        self.addUrl(item)
        self.addParam(item)
        self.sign_data(item)
        self.getDelayTime(item)
        self.res.append(item)

    def addParam(self, item):
        try:
            db = item['fetch_data_from_db']
            if db:
                db = eval(db)
                item["fetch_data_from_db"] = db
                dbutils.DBHandler(item).query()

            apiInfo = self.getApiInfo(item)

            orginParam = apiInfo['defualt_param']

            orginParam = orginParam if orginParam else '{}'
            tempparam = eval(orginParam)
            user_param = item['params']

            predb = item['preReadyData']
            if predb:
                predb = eval(predb)
                item["preReadyData"] = predb
                dbutils.DBHandler(item).dealSql(predb)
            if user_param:
                new_dict = addict.Dict(tempparam)
                list_param = {}
                if "," in user_param:
                    list_param = user_param.split(',') if user_param else {}
                else:
                    list_param = [user_param]
                list_param = list(map(lambda x: 'new_dict' + x[1:], list_param))
                list_param = list(map(lambda x: re.sub(r'\$', '', x), list_param))

                for x in list_param:
                    logging.info(f'x is {x}')

                    key, value = x.split('=')
                    valueAll = value
                    # 从字典中去找对应的变量进行替换  '${#customerName}'
                    resdict = re.findall(r'\{#(.*)\}', value)
                    if resdict:
                        kw = resdict[0]

                        # value = globalData.globalsData[kw]
                        value = redisutils.myredis.hmget('params', kw)
                        value = value if value else ""
                        value11 = re.sub(r'\{#(.*)\}', value, valueAll)

                        x = '='.join((str(key), value11))
                        exec(x)

                    res = re.findall(r'\{__(.*)\((.*?)\)?\}.*', value)

                    # 调用随机数据生成函数来替换变量
                    if res:

                        fun = res[0][0]
                        params = ''
                        if len(res[0]) > 1:
                            params = res[0][1]
                        obj = getattr(myDataUtils, 'DataUtils')()
                        md = getattr(obj, fun)
                        if params:
                            value = md(params)
                        else:
                            value = md()  # 这里调用方法，可以传入参数
                        x = '='.join((str(key), repr(value)))
                        kw = key.split('.')[-1]
                        globalData.globalsData[kw] = value
                        a = {kw: value}

                        redisutils.myredis.hmset('params', a)

                    exec(x)

                item['params'] = new_dict

            else:

                item['params'] = tempparam
        except Exception as e2:

            logging.error(e2.args)

    def cfg_case(self):
        for item in self.caselist:
            self.handle(item)

    # 拼接环境域名和接口URL
    def addUrl(self, item):
        apiInfo = self.getApiInfo(item)
        baseUrl, dbenv = self.getEnv(item)
        all_url = baseUrl + apiInfo['url']
        item['URL'] = all_url
        item['DBEnv'] = dbenv

    # 根据环境id获取环境名称
    def getEnv(self, item):
        envId = item['envId']
        envInfo = list(filter(lambda x: x['envId'] == envId, self.envList))[0]
        return envInfo['host'] if envInfo['host'] else {}, envInfo['dbconfig'] if envInfo['dbconfig'] else {}

    @staticmethod
    def save_req_res(src_req, req, r):
        is_json = True
        try:
            response1 = json.dumps(r.json(), indent=3, ensure_ascii=False)
            response = r.json()
        except Exception as e:
            print("响应不是json")
            is_json = False


        temp = {}

        if src_req:

            src_reqlist = src_req.split(',')
            for item in src_reqlist:

                var1 = ""

                if '=' not in item:
                    var1 = item.split('.')
                    key = var1[-1].strip()
                    key2 = key
                else:
                    var1 = item.split("=")[1].split(".")
                    key = var1[-1].strip()
                    key2 = item.split("=")[0].split(".")[-1].strip()
                type = var1[1]

                pattern = '$..{}'.format(key)

                # values = jsonpath.jsonpath(req, pattern) if type == 'req' else jsonpath.jsonpath(response, pattern)
                if type == 'req':
                    if is_json:
                        values = jsonpath.jsonpath(req, pattern)
                elif type == 'res':
                    if is_json:

                        values = jsonpath.jsonpath(response, pattern)
                    else:
                        pass
                elif type == 'header':
                    values=[]
                    pattern = key
                    values.append(r.headers.setdefault(f'{pattern}', None))
                    logging.info(values)

                if not values:
                    return

                logging.info(f'要存储的数据为{key2}：{values[0]}---{values}')
                if len(values) == 1:
                    redisutils.myredis.hmset('params', {str(key2): str(values[0])})
                    temp[key2] = values[0]
                elif len(values) > 1:
                    for x in range(values):
                        if x == 0:
                            redisutils.myredis.hmset('params', {key2: str(values[0])})
                            temp[key2] = values[0]
                        else:
                            redisutils.myredis.hmset('params', {key2 + str(x): str(values[x])})
                            temp[key2] = values[x]
            logging.info('中间变量保存成功')

    def getDelayTime(self, item):
        apiInfo = self.getApiInfo(item)
        delayTime = apiInfo['delayTime']
        item['delayTime'] = delayTime if delayTime else 0
