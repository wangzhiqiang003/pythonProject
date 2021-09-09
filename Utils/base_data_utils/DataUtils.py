import datetime
import random
import time

import json

from name import Name
from identity import IdNumber
from BankCardNumber import GetBankCardNumber
import faker
import re
import hashlib

myfaker = faker.Faker(locale='zh_CN')


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
        return bank_no

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
        return DataUtils.get_random_name()+myfaker.company()

    def md5(self, data):
        md5hash = hashlib.md5()
        data = json.dumps(data)
        md5hash.update(data.encode())
        md5 = md5hash.hexdigest()
        return md5

    @staticmethod
    def get_random_before_date():
        # temp = str(random.randint(1990, 2021))
        # print(temp)
        # date = myfaker.credit_card_expire()
        # date = f'{temp}/{date}'
        # print(date)
        # date = time.strptime(date, '%Y/%m/%d')
        # date = time.strftime('%Y-%m-%d', date)
        # return date

        time = datetime.datetime.now()
        dt = datetime.timedelta(days=-(360*random.randint(5,20)))
        time = time + dt
        time =time.strftime('%Y-%m-%d')
        return  time


if __name__ == '__main__':
    # print(DataUtils.get_random_name())
    # print(DataUtils.get_random_id())
    print(DataUtils.get_bank_no())
    # bankToBin = json.load(open("json/banknametobin.json", 'r', encoding='utf-8'))
    # print(bankToBin)
    #
    # print(DataUtils.get_random_id())
    # print(DataUtils().get_bank_no())

    print(DataUtils.get_random_id())
    print(DataUtils.get_bank_no())
