from base_data_utils import BankCardNumber

if __name__ == '__main__':
    # test = BankCardNumber.GetBankCardNumber()
    # print(test.getBankCardNumber(useRandom=False),end='')

    import  xlrd3 as xlrd
    s = xlrd.open_workbook("a.xls",ignore_workbook_corruption=True)