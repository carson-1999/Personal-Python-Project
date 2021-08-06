import  requests
from urllib import  parse
from urllib import request
import  os  #os常用来控制操作系统,如对文件夹的各种操作


headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
,'referer': 'https://pvp.qq.com/web201605/wallpaper.shtml'
}

"""封装函数，获取图片的url"""
def extract_images(data):
    images_urls = []
    #从1~8，因为每个图片的url经过json解析了sProImgNo_（1~8)
    for x in range(1,9):
        image_url = parse.unquote(data['sProdImgNo_%d'%x])
        image_url = image_url.replace("200","0")
        images_urls.append(image_url)
    return images_urls


def main():
    #写下对应文件的Request_url
    page_url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page=0&iOrder=0&iSortNumClose=1&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1595339742487'
    resp = requests.get(page_url,headers = headers)   #返回的对象文本内容和之前json解析response一样的内容
    #所以想要删除文本开头的函数得到其json内容的话，删除url相关的jsoncallback后的(参数名字和内容)即可
    #于是成功删除前面的函数内容，只得到json内容
    #通过json()方法，将本能够转换成字典的json内容转换成字典
    result = resp.json()
    #提取数据，提取字典中的List键，前面分析json解析数据得图片名字字符串信息就在这里
    datas = result['List']
    for data in datas:
        image_urls = extract_images(data)
        #打印图片对应的名字，名字在List的object的sProName键,其内容仍是被编码过的字符串
        #故需对名字进行解码
        name = parse.unquote(data['sProdName'])
        #os模块的os.path.join()进行路径的拼接
        dirpath = os.path.join("images",name)
        #os.mkdir()方法创建文件夹，images/猪八戒,即在这images里面根据角色名字创建文件夹
        os.mkdir(dirpath)
        #下载图片,用到enumerate()返回两个值，获取下标
        for index,image_url in enumerate(image_urls):
            request.urlretrieve(image_url,os.path.join(dirpath,'%d.jpg'%(index+1)))
            print("%s下载完成"%name)


if __name__ == '__main__':
    main()