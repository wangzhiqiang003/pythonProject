from requests import *
import  hashlib
import  requests
import  json
baseurl = 'http://api-dev.runthinkenv.com/api/riskApproval/selection/preCredit/enterprise/create'

headers={

  "Content-Type": "application/json;charset=UTF-8",
  "Authorization": "bearer  ecde5707-3567-4d88-bf04-445bac41eb6d"



}


# data ="{\"tradeType\":12,\"tradeScope\":5,\"channelCode\":\"XSH001\",\"customClassify\":\"0\",\"customerName\":\"sdfffsdfd\",\"certificateType\":\"A18\",\"certificateCode\":\"510311199003235699\",\"preCreditResult\":1,\"preCreditAmount\":\"11111\",\"repaymentMethods\":[{\"loanPeriods\":[\"1\",\"100\"],\"periodType\":\"1\",\"repaymentType\":\"30\"}],\"yearRate\":\"10\",\"closingTime\":\"2025-08-30 23:59:59\",\"status\":1,\"preCreditEnterpriseInfo\":{\"organizationType\":\"1\",\"industryType\":1,\"tradeType\":7,\"legalPersonName\":\"账单\",\"legalPersonMobile\":\"13568895445\",\"legalPersonCertType\":\"B01\",\"legalPersonCertNum\":\"510311199003234512\",\"loanBankCreateName\":\"中国建设银行平顶山建设路支行\",\"loanBankName\":\"中国建设银行\",\"loanBankCreateCode\":\"105495000020\",\"loanBankCreateProvence\":\"河南省\",\"loanBankCreateCity\":\"平顶山市\",\"loanBankCustomerName\":\"是发范德萨\",\"loanBankCardNum\":\"1122121212\",\"establishDate\":\"2021-08-11\",\"registeredCapital\":\"200000\",\"registeredAddr\":\"1235\",\"tradeScope\":7,\"channelCode\":\"XSH001\",\"loanBankCode\":\"CCB\"}}"
data ={
  "tradeType": 12,
  "tradeScope": 5,
  "channelCode": "XSH001",
  "customClassify": "1",
  "customerName": "的人few热",
  "certificateType": "A18",
  "certificateCode": "510311199003235432",
  "status": 1,
  "preCreditEnterpriseInfo": {
    "organizationType": "5",
    "industryType": 1,
    "tradeType": 6,
    "legalPersonName": "士大夫",
    "legalPersonMobile": "15244145120",
    "legalPersonCertType": "B01",
    "legalPersonCertNum": "410185197509131642",
    "loanBankCreateName": "中国建设银行玉溪建设支行",
    "loanBankName": "中国建设银行",
    "loanBankCreateCode": "105741000042",
    "loanBankCreateProvence": "云南省",
    "loanBankCreateCity": "玉溪市",
    "loanBankCustomerName": "622676761501080105472",
    "loanBankCardNum": "622676761501080105472",
    "tradeScope": 6,
    "registeredAddr": "手动阀手动阀",
    "channelCode": "XSH001",
    "loanBankCode": "CCB",
    "provence": "110000",
    "city": "110100"
  }
}

# data ="{\"tradeType\":12,\"tradeScope\":5,\"channelCode\":\"XSH001\",\"customClassify\":\"0\",\"customerName\":\"111\",\"certificateType\":\"A18\",\"certificateCode\":\"510311199003234512\",\"preCreditResult\":1,\"preCreditAmount\":\"1000\",\"repaymentMethods\":[{\"loanPeriods\":[\"1\",\"100\"],\"periodType\":\"1\",\"repaymentType\":\"30\"}],\"yearRate\":\"10\",\"closingTime\":\"2022-08-27 23:59:59\",\"status\":1,\"preCreditEnterpriseInfo\":{\"contactCertType\":null,\"organizationType\":\"1\",\"industryType\":2,\"tradeType\":2,\"legalPersonName\":\"风格和\",\"legalPersonMobile\":\"13568890221\",\"legalPersonCertType\":\"B01\",\"legalPersonCertNum\":\"510311199003234512\",\"loanBankCreateName\":\"中国建设银行平顶山建设路支行\",\"loanBankName\":\"中国建设银行\",\"loanBankCreateCode\":\"105495000020\",\"loanBankCreateProvence\":\"河南省\",\"loanBankCreateCity\":\"平顶山市\",\"loanBankCustomerName\":\"6227002432220410613\",\"loanBankCardNum\":\"6227002432220410613\",\"establishDate\":\"2021-08-01\",\"registeredCapital\":\"20000\",\"registeredAddr\":\"200000\",\"tradeScope\":7,\"channelCode\":\"XSH001\",\"loanBankCode\":\"CCB\"}}"











print(data)
h =hashlib.md5()
h.update(json.dumps(data).encode())
signkey =h.hexdigest()
print(signkey)
headers['runthink-sign']=signkey
print(headers)
r =requests.post(baseurl,headers=headers,data=json.dumps(data))
print(r.headers)
print(r.json())


