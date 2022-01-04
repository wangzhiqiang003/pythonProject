import execjs
pkey ='''
ab'''
Passwd = execjs.compile(open(r"test.js").read()).call('encrypt',pkey)
print(Passwd)