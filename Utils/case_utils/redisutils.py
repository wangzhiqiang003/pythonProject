import logging
import pickle
from unicodedata import decimal
from decimal import *

import redis
from redis import Redis

r = redis.Redis()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='myapp.log',
                # filemode='w'
                    )
class MyRedis():
    def __init__(self, ip, passwd, port=6379, db=0):
        # 构造函数
        try:
            self.r = redis.Redis(host=ip, password=passwd, port=port, db=db)

        except Exception as e:
            print('redis连接失败，错误信息%s' % e)

    def str_get(self, k):
        res = self.r.get(k)
        if res:
            return res.decode()

    def str_set(self, k, v, time=None):
        self.r.set(k, v, time)

    def delete(self, k):
        tag = self.r.exists(k)  # 判断这个Key是否存在
        if tag:
            self.r.delete(k)
            print('删除成功')
        else:
            print('这个key不存在')

    def hash_hget(self, name, key):
        res = self.r.hget(name, key)
        if res:
            return res.decode()

    def hmset(self, name, k):
        # self.r.hmset(name, k)
        try:
            self.r.hmset("params", k)
        except DeprecationWarning as e:
            logging.info(e)

    def hmget(self, name,key):
        res = self.r.hget(name,key=key)
        # res = pickle.load(res)
        if res:
            return res.decode()

    def hash_hset(self, name, k, v):
        self.r.hset(name, k, v)

    def hash_getall(self, name):
        res = self.r.hgetall()
        new_dict = {}
        if res:
            for k, v in res.items():
                k = k.decode()
                v = v.decode()
                new_dict[k] = v
        return new_dict

    def hash_del(self, name, k):
        res = self.r.hdel(name, k)
        if res:
            print('删除成功')
            return True
        else:
            print('删除失败.该key不存在')
            return False

    @property
    def clean_redis(self):
        self.r.delete('params')
        self.r.flushdb()  # 清空redis
        print('清空redis成功.')


myredis = MyRedis('127.0.0.1', passwd='test123')
if __name__ == '__main__':
    a = MyRedis('127.0.0.1', passwd='test123')

    print(a.hmget('params', key="issuedBy"))

