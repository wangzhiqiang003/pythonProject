import json


def replace_data(fn):
    def func(*args, **kwargs):
        print("==================================================")
        print(args[1])

        print("==================================================")
        return fn(*args, **kwargs)

    return func

def get_target_value(key, dic, tmp_list):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    else:
        for value in dic.values():  # 传入数据不符合则对其value值进行遍历
            if isinstance(value, dict):
                get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list


def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身


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
        return apiInfo

    @replace_data
    def addHeader(self, item):
        apiInfo = self.getApiInfo(item)
        tempparam = eval(apiInfo['defaultHeader'])
        tempparam.update(eval(str(item['headers'])))
        item['headers'] = tempparam

    def handle(self, item):
        self.addHeader(item)
        self.addParam(item)
        self.addUrl(item)
        self.res.append(item)

    @replace_data
    def addParam(self, item):
        apiInfo = self.getApiInfo(item)
        tempparam = eval(apiInfo['defualt_param'])
        tempparam.update(eval(item['params']))
        item['params'] = tempparam
        print(item)

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
        envInfo = list(filter(lambda x: x['envId'], self.envList))[0]
        return envInfo['host']
