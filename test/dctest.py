import logging
import uuid

import pymysql

import DataUtils


class DBHandler:
    def __init__(self, database):
        self.database = database
        self.createDB()

    def query(self):
        pass

    def createDB(self):
        try:

            ip = "192.169.6.33"
            port = 3306
            user = "root"
            passwd = "runthink@2020"
            charset = "utf8"
            dbName = self.database

            self.conn = pymysql.connect(

                host=ip,
                user=user,
                password=passwd,
                database=dbName,
                charset=charset,
                port=port,
                autocommit=True

            )
            self.cursor = self.conn.cursor()


        except Exception as e:
            logging.error(e)

    def dealSql(self, sql):
        self.cursor.execute(sql)


if __name__ == '__main__':
    # from pyDes import des, PAD_PKCS5, ECB
    #
    # DES_SECRET_KEY = '1234567890123456'
    # s = '13568890221'.encode()  # 这里中文要转成字节， 英文好像不用
    # des_obj = des(DES_SECRET_KEY, ECB, DES_SECRET_KEY, padmode=PAD_PKCS5)
    # secret_bytes = des_obj.encrypt(s)
    # s = des_obj.decrypt(secret_bytes)
    # print(secret_bytes.hex())
    # print(s.decode())
    # # d = DataUtils.DataUtils()

    for i in range(1):
        d = DataUtils.DataUtils()
        payername = d.get_random_company_name()
        payercode = d.get_random_id()
        legalpserson = d.get_random_name()
        legId = d.get_random_id()
        legphone = d.get_random_phone()
        contactperson = d.get_random_name()
        contactpersonID = d.get_random_id()
        contactpersonphone = d.get_random_phone()
        bankaccount = d.get_bank_no()

        receivercompany = d.get_random_company_name()
        receivercompanyaccount = d.get_bank_no()
        receivercompanyCode = d.get_random_id()
        receivercompanyCode = d.get_random_id()
        receivercompanyCode = d.get_random_id()
        payercode = d.get_random_id()
        legalpserson1 = d.get_random_name()
        legalpserson1phone = d.get_random_phone()
        legalpserson1Id = d.get_random_id()
        company_contacts = d.get_random_name()
        company_contactsId = d.get_random_id()
        company_contactsph = d.get_random_phone()
        addr = d.get_random_addrs()
        c1 =str(uuid.uuid4()).upper()
        c2=str(uuid.uuid4()).upper()
        c3=str(uuid.uuid4()).upper()
        print(c1)

        # 支付企業
        sql = f'''
        INSERT INTO dev_scdb.ads_prov_payerlegalinfo (payer_no, data_update_time, payer_name, payer_social_credit_code,
                                              is_wholly_owned, joint_company, shareholding_ratio, function_type,
                                              payer_legal_representative, payer_legal_representative_id,
                                              payer_legal_representative_phone, payer_contact_name, payer_contact_id,
                                              payer_contact_phone, payer_address, payer_account_no, payer_account_name,
                                              payer_beneficiary_bank_name, create_time)
VALUES ('{c1}', date_format(date_add(now(),interval -1 day), '%Y-%m-%d'), '{payername}', '{payercode}', 0, null, 0.50,
        null, '{legalpserson}', '{legId}', '{legphone}', '{contactperson}', '{contactpersonID}', '{contactpersonphone}',
        '中国（云南）自由贸易试验区昆明片区经开区经开路3号科技创新园A35-A203', '{bankaccount}', '{payername}',
    '中国建设银行云南省分行昆明市北京路支行', now());
        '''
        # 供應商
        sql2 = f'''
INSERT INTO dev_scdb.ads_prov_suplierinfo (suplier_no, data_update_time, supplier_name, social_credit_code,
                                           receiving_account_no, receiving_account_name, beneficiary_bank_name,
                                           cooperation_year, company_type, sector, industry, internal_grade,
                                           supplier_province, register_addr, whether_dispute, supplier_catgory,
                                           contract_amount_rank, legal_representative, legal_representative_phone,
                                           legal_representative_id, company_contacts, company_contacts_phone,
                                           company_contacts_id, contacts_position, create_time)
VALUES ('{c2}', date_format(date_add(now(),interval -1 day), '%Y-%m-%d'), '{receivercompany}', '{receivercompanyCode}','{receivercompanyaccount}', '{receivercompany}', '华夏银行股份有限公司深圳泰然支行', 0.00, '0', '2',
        '2', null, '广东省', '{addr}', null, '公区装修工程,幕墙工程,大区批量精装修工程', 3, '{legalpserson1}', '{legalpserson1phone}', '{legalpserson1Id}', '{company_contacts}',
     '{company_contactsph}', '{company_contactsId}', null,
        now());

                '''

        sql3 = f'''
        INSERT INTO dev_scdb.ads_prov_suplierpaidinfo (data_update_time, suplier_no, supplier_name, social_credit_code,
                                               contract_name, contract_no, amount_on_contract, contract_start_date,
                                               completion_date, total_ouput_vlaue, total_paid_amount, total_paid_ratio,
                                               total_payable_amount, estimated_settlement_amount,
                                               estimated_retention_amount, whether_pledge, payer_no, payer_name,
                                               payer_social_credit_code, create_time)
VALUES (date_format(date_add(now(),interval -1 day), '%Y-%m-%d'), '{c2}', '{receivercompany}', '{receivercompanyCode}', '昆明上品2号楼装修合同',
       '{c3}', 5500000.00, '2021-11-25', '2022-12-25', 4500000.00, 1000000.00, 0.20,
        1500000.00, 3000000.00, 1000000.00, 1, '{c1}', '{payername}',
        '{payercode}',now());
        '''
        print(sql2)

        db = DBHandler('dev_scdb')
        db.dealSql(sql)
        db.dealSql(sql2)
        db.dealSql(sql3)
