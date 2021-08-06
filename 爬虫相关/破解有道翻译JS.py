# requests

# pip install requests

import requests
import time
import random
import hashlib

word = input("请输入你要翻译的单词：")
url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
	"Referer": "http://fanyi.youdao.com/?keyfrom=fanyi-new.logo",
	"Origin": "http://fanyi.youdao.com",
	"Cookie": "OUTFOX_SEARCH_USER_ID=1992865268@182.87.173.10; OUTFOX_SEARCH_USER_ID_NCOO=2134926802.2224576; _ga=GA1.2.359522511.1518241590; P_INFO=18570631587|1540190771|2|study|00&99|CN&1540177284&study#US&null#10#0#0|&0|null|18570631587; _ntes_nnid=448b22d901e81b2cabd649e507632f40,1541835430513; fanyi-ad-id=52077; fanyi-ad-closed=1; _gid=GA1.2.504190165.1542015730; JSESSIONID=aaaNJKlLmdf7SeYGZ8hCw; ___rl__test__cookies=1542027032131"
}
salt = str(int(time.time()*1000) + random.randint(1,9))
temp = "fanyideskweb" + word + salt + "sr_3(QOHT)L2dx#uuGR@r"
sign = hashlib.md5(temp.encode("utf-8")).hexdigest()
formdata = {
	"i": word,
	"from": "AUTO",
	"to": "AUTO",
	"smartresult": "dict",
	"client": "fanyideskweb",
	"doctype": "json",
	"version": "2.1",
	"keyfrom": "fanyi.web",
	"action": "FY_BY_REALTIME",
	"typoResult": "false",
	"salt": salt,
	"sign": sign
}
response = requests.post(url=url,headers=headers,data=formdata)
print(response.text)