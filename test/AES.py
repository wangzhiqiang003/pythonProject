import re

a =r'.*#access_token=(?P<access_token>(.*?))&token_type=(?P<token_type>(.*?))&.*'
b = 'http://riskapproval-dev.runthinkenv.com/redirect?target_url=http://riskapproval-dev.runthinkenv.com/dashboard#access_token=f7a0d532-4e29-466f-a792-b82754e57c0f&token_type=bearer&expires_in=999&scope=all'


res = re.match(a,b)
print(res.groupdict())



print(str(None))