from base_data_utils import BankCardNumber
import requests
import urllib

if __name__ == '__main__':
    import requests

    url = "https://api.runthink.xyz/api/riskApproval/receive/accounts/batchImport"
    files = {"file": (
        open('./case/account.xlsx', 'rb'))
    }

    r = requests.request(method='post', url=url, files=files, headers={
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryJFXydeRYN11fkAFb",
        "Authorization": "Bearer a48c0333-6781-4d52-9df6-9b933896e3a4"})

    print(r.headers)
    #
    # payload = "id=2&executorParam="
    # headers = {
    #     'Content-Type': "application/x-www-form-urlencoded",
    #     'Cookie': "XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d",
    #
    # }
    #
    # response = requests.request("POST", url, data=payload, headers=headers)
    #
    # print(response)
