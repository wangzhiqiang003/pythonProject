import json

from name import Name
from identity import IdNumber
from BankCardNumber import GetBankCardNumber
import  json
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


if __name__ == '__main__':
    # print(DataUtils.get_random_name())
    # print(DataUtils.get_random_id())
    # print(DataUtils.get_bank_no())
    # bankToBin = json.load(open("json/banknametobin.json", 'r', encoding='utf-8'))
    # print(bankToBin)

    print(DataUtils.get_random_id())
    print(DataUtils.get_bank_no())
