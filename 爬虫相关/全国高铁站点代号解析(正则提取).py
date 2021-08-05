import re
import  requests

#根据12306的network的某个文件response得到请求的url
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9151'
resp = requests.get(url)
text = resp.text
#print(text)
#正则表达式提取三字符代号
it = re.findall(r'@\w{3}\|.{2,5}\|\w{3}',text)
for x in it:
    x = x.replace('@','')
    print(x)
#findall()方法解析
"""for match in it:
    match_group = match.group()
    # (去掉@)从"@bjb|北京北|VAP"过滤数据，得到"bjb|北京北|VAP"这样形式的数据
    num = re.sub(r'@','',match_group)
    # (变空格)从"bjb|北京北|VAP"过滤数据，得到"bjb 北京北 VAP"这样形式的数据,注意|前面加\
    num = re.sub(r'\|',' ',num)
    # 将"bjb 北京北 VAP"这个数据中的非空格的字符串取出,变成了一个一个的字符串
    num = re.finditer(r"(\S){2,5}", num)
    #创建空列表，添加前面拆出来的单个的字符串,变成列表后方便后面根据下标提取数据
    list = []
    for num1 in num:
        list.append(num1.group())
    #前面已经将三个数据转换成了列表，根据下标提取出如’北京北‘，’VAP‘的形式
    #里面有个异常的两个数据的列表，要俘获异常
    try:
        station_name = list[1]
        station_code = list[2]
        print((station_name,station_code))
    except:
        pass"""




