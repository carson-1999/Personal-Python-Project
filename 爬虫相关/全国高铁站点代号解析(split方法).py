import  requests

#运用split方法和切片分割提取数据
def get_codes(f):
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9151'
    resp = requests.get(url)
    results = resp.text
    results = results.split('@')
    for result in results[1:]:
        station = result.split('|')
        name = station[1]
        code = station[2]
        f.write('{},{}\n'.format(name, code))
        # print((name,code))


def main():
    with open('全国车站.csv','a',encoding='utf-8') as f:
        f.write('{},{}\n'.format('name','code'))
        get_codes(f)

if __name__ == '__main__':
    main()


