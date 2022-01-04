import decimal
import json
import logging
import re

import pymysql
import redisutils
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='myapp.log',
                # filemode='w'
                    )


class DBHandler:
    def __init__(self, item):

        self.item = item
        self.conn = None
        super().__init__()

    def query(self):

        sqllist = self.item['fetch_data_from_db']['data']
        dict_res = {}
        for dbvo in sqllist:
            try:
                database = dbvo['DBName']
                self.createDB(self.item, database)
                sql = dbvo['sql']
                parmlist = dbvo['param']
                logging.info(type(parmlist))
                parmlist_bak = []
                for p in parmlist:
                    resdict = re.findall(r'\{#(.*)\}', p)
                    if resdict:
                        kw = resdict[0]

                        # value = globalData.globalsData[kw]
                        value = redisutils.myredis.hmget('params', kw)
                        value11 = re.sub(r'\${#(.*)\}', value, p)
                        parmlist_bak.append(value11)
                    else:
                        parmlist_bak.append(p)
                if parmlist_bak:
                    parmlist = parmlist_bak
                res = self.cursor.execute(query=sql, args=parmlist)


                desclist = [desc[0] for desc in self.cursor.description]

                if res == 1:
                    dbres = self.cursor.fetchone()

                    # dbres = [str(x) for x in dbres]
                    dictres = dict(zip(desclist, dbres))
                    logging.info(dictres)

                    self.saveparamtoredis(dictres)
                else:
                    dbres = self.cursor.fetchall()

                    for index in range(len(dbres)):
                        desclist_Name = [f'{desc[0]}_{index}' for desc in self.cursor.description]
                        oneData = dict(zip(desclist_Name, dbres[index]))
                        self.saveparamtoredis(oneData)
                        logging.info(f'{index} ---as---{dbres[index]}')  # 这里要补充多条记录存的逻辑，redis后面还是要改成bson格式，不然不好扩展
            except Exception as e:
                logging.info(e)

            # cursor.execute

    def createDB(self, item, databasse):
        try:

            dbconfig = item['DBEnv']
            dbconfig = eval(dbconfig)
            ip = dbconfig['ip']
            port = dbconfig['port']
            user = dbconfig['user']
            passwd = dbconfig['passwd']
            charset = dbconfig['charset']
            dbName = databasse

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
        sqllist = self.item['preReadyData']['data']
        dict_res = {}
        for dbvo in sqllist:
            try:
                logging.error(dbvo)
                database = dbvo['DBName']
                self.createDB(self.item, database)
                sql = dbvo['sql']
                parmlist = dbvo['param']
                parmlist_bak = []
                for p in parmlist:
                    resdict = re.findall(r'\{#(.*)\}', p)
                    if resdict:
                        kw = resdict[0]

                        # value = globalData.globalsData[kw]
                        value = redisutils.myredis.hmget('params', kw)
                        value11 = re.sub(r'\${#(.*)\}', value, p)
                        parmlist_bak.append(value11)
                if parmlist_bak:
                    parmlist = parmlist_bak
                res = self.cursor.execute(query=sql, args=parmlist)

                logging.info(f'paramllistsfsdf{type(parmlist)}')
                res = self.cursor.execute(query=sql, args=parmlist)



            except Exception as e:
                logging.info(e)

    def saveparamtoredis(self, res):

        # new_dict = {x: float(y) for x, y in res.items() if type(y) == decimal.Decimal}
        new_dict = {x: str(y) for x, y in res.items()}

        res.update(new_dict)

        myrds = redisutils.myredis

        # print(b)
        # value = json.dumps(res)
        myrds.hmset('params', res)
        logging.info(f'存入的值为{new_dict}')
