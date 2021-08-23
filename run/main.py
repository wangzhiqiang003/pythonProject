import os.path
import pprint

from caseAssemble import CaseAssemble
from case_utils.excelutils import *

if __name__ == '__main__':
    e = ExcelUtils("../case/API_CASE_INFO.xlsx")
    t=e.assemble_info()
    bean =CaseAssemble(t)
    bean.cfg_case()
    print(bean.res)


