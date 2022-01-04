#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'wangzhiqiang'

import logging
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(BASE_DIR)

# 配置文件
TEST_CONFIG =  os.path.join(BASE_DIR,"database","config.ini")
# 测试用例模板文件
SOURCE_FILE = os.path.join(BASE_DIR,"database","DemoAPITestCase.xls")
# excel测试用例结果文件
TARGET_FILE = os.path.join(BASE_DIR,"report","excelReport","DemoAPITestCase.xls")
# 测试用例报告
TEST_REPORT = os.path.join(BASE_DIR,"report")
# 测试用例程序文件
TEST_CASE = os.path.join(BASE_DIR,"suite")


CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://192.168.10.2:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "CONNECTION_POOL_KWARGS": {"max_connections": 512},
                "IGNORE_EXCEPTIONS": True,
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
            }
        },
        "authority": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://192.168.10.2:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "CONNECTION_POOL_KWARGS": {"max_connections": 512},
                "IGNORE_EXCEPTIONS": True,
                "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
                "SOCKET_TIMEOUT": 5,  # in seconds
            }
        },
        "feedflow": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://192.168.10.2:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "CONNECTION_POOL_KWARGS": {"max_connections": 512},
                "IGNORE_EXCEPTIONS": True,
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
            }
        },
    }




