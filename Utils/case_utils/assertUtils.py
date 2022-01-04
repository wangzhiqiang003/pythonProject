import logging
import unittest
from addict import Addict
import json


class AssertUtils(unittest.TestCase):
    def __init__(self):
        pass

    def assertJson(self, response, expectdata):
        try:
            res = Addict(response, ensure_ascii=False, indent=2)
            expectPaht, value = expectdata.split('=')

            resValue = repr(eval('res' + str(expectPaht[1:])))

            return value == resValue

        except Exception as e:
            return False
