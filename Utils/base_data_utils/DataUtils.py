# coding:utf-8
import base64
import datetime
import random

import json
from base64 import b64decode
from Cryptodome.PublicKey import RSA

import redisutils
from name import Name
from identity import IdNumber
from BankCardNumber import GetBankCardNumber
import faker
import re
import hashlib
from Cryptodome.Cipher import PKCS1_v1_5 as PKCS1_cipher

myfaker = faker.Faker(locale='zh_CN')

import urllib
import execjs


class DataUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_random_name():
        return ''.join(Name.random_name())

    @staticmethod
    def get_random_id():
        return IdNumber.generate_id()

    @staticmethod
    def get_bank_no(binNum='622676'):
        bank_no = GetBankCardNumber(binNum).getBankCardNumber()
        return bank_no[:16]

    @staticmethod
    def get_random_phone():
        return myfaker.phone_number()

    @staticmethod
    def get_random_addrs():
        res = myfaker.address()
        return res.split(' ')[0]

    @staticmethod
    def get_random_mail():
        return myfaker.ascii_company_email()

    @staticmethod
    def get_random_company_name():
        return DataUtils.get_random_name() + myfaker.company()

    def md5(self, data):
        md5hash = hashlib.md5()
        data = json.dumps(data)
        md5hash.update(data.encode())
        md5 = md5hash.hexdigest()
        return md5

    @staticmethod
    def get_random_before_date():
        time = datetime.datetime.now()
        dt = datetime.timedelta(days=-(360 * random.randint(5, 20)))
        time = time + dt
        time = time.strftime('%Y-%m-%d')
        return time

    @staticmethod
    def encript(pwd):
        publicKey = redisutils.myredis.hmget('params', "publicKey")
        print(publicKey)
        key = base64.urlsafe_b64decode(publicKey)
        rsakey = RSA.importKey(key)
        print(rsakey)
        cipher = PKCS1_cipher.new(rsakey)  # 生成对象
        cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
        value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
        print(value)
        return value

    @classmethod
    def tojson( content):
        if content:
            return json.loads(content)
        else:
            return ""


if __name__ == '__main__':
    # print(DataUtils.encrypt('q1111111',
    #                         'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7jO8tS2ZSPBC5wwPBIK_rHciIEJ2m_r0xgMUUFTaFgW-T9eUSIQyqtAknBGjt0Ipu1GRjYJeBftRFjNGbfV_w8bLpPb3gbhW9e_lYsWKy_dty5J9dBzCst57W64tRDh5z8dFwgidO7sOLNou0wYGIsY08Hko29xKFGkc66s-VZAFbiZ9utu9Gf8dhTBiOWVuMjLQ_E3MPw7NTV9RQKJhtYaXAmX7uojlOYKtVLAyrnMIuwMHKSWdvfuOAOt6JWlCm_tcD1-fRXhf8LrSKCi-iiqtSLy4F30qk_NuJUYMP-f55WhTcLtAAoDEkU205vfNcSoaZO1SLm5-D8xXX70U3QIDAQAB'.encode('utf8').decode('utf8')))
    # print(DataUtils.get_bank_no())
    # print(DataUtils.get_bank_no())
    # print(DataUtils.get_bank_no())
    # print(DataUtils.get_bank_no())
    print(DataUtils.get_bank_no())
    # print(DataUtils.get_bank_no())
    print('=======================')
    print(DataUtils.get_random_id())
    # print(DataUtils.get_random_id())
    # print(DataUtils.get_random_id())
    # print(DataUtils.get_random_id())
    # print(DataUtils.get_random_phone())
    # print(DataUtils.get_random_phone())
    print(DataUtils.get_random_company_name())
    # print(DataUtils.get_random_name())
    # print(DataUtils.get_random_name())
    # print(DataUtils.get_random_addrs())
    # print(DataUtils.get_random_mail())
    for i in range(100):
        with open('companyinfo.txt', 'a') as f:
            companyname = DataUtils.get_random_company_name()
            f.write(f'公司名称:{companyname}' + '\n')
            f.write(f'社会信用代码:{DataUtils.get_random_id()}' + '\n')
            f.write(f'联系人姓名:{DataUtils.get_random_name()}' + '\n')
            f.write(f'联系人身份证号:{DataUtils.get_random_id()}' + '\n')
            f.write(f'联系人手机号:{DataUtils.get_random_phone()}' + '\n')
            f.write(f'联系人姓名:{DataUtils.get_random_name()}' + '\n')
            f.write(f'联系人身份证号:{DataUtils.get_random_id()}' + '\n')
            f.write(f'联系人手机号:{DataUtils.get_random_phone()}' + '\n')
            f.write(f'联系人姓名:{DataUtils.get_random_name()}' + '\n')
            f.write(f'联系人身份证号:{DataUtils.get_random_id()}' + '\n')
            f.write(f'银行卡号:{DataUtils.get_bank_no()}' + '\n')
            f.write(f'开户名:{companyname}' + '\n')
            f.write(f'开户银行:和平县农村信用合作联社东水信用社' + '\n')
            f.write('\n')
            f.write('\n')
