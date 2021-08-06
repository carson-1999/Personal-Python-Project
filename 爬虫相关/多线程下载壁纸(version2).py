import  requests
from urllib import  parse
from urllib import request
import  os  #os常用来控制操作系统,如对文件夹的各种操作
import threading
from queue import  Queue

"""生产者,生产url"""
class Producer(threading.Thread):
    def __init__(self,page_queue,image_queue,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.image_queue = image_queue

    def run(self) -> None:
        while not self.page_queue.empty():
            page_url = self.page_queue.get()
            resp = requests.get(page_url, headers=headers)  # 返回的对象文本内容和之前json解析response一样的内容
            # 所以想要删除文本开头的函数得到其json内容的话，删除url相关的jsoncallback后的(参数名字和内容)即可
            # 于是成功删除前面的函数内容，只得到json内容
            # 通过json()方法，将本能够转换成字典的json内容转换成字典
            result = resp.json()
            # 提取数据，提取字典中的List键，前面分析json解析数据得图片名字字符串信息就在这里
            datas = result['List']
            for data in datas:
                image_urls = extract_images(data)
                # 打印图片对应的名字，名字在List的object的sProName键,其内容仍是被编码过的字符串
                # 故需对名字进行解码,注意图片文件夹名防止特殊符号,需替换掉:和去掉空格等操作
                name = parse.unquote(data['sProdName']).replace("1:1",'').strip()
                # os模块的os.path.join()进行路径的拼接
                dir_path = os.path.join("images", name)
                # os.mkdir()方法创建文件夹，(images/猪八戒),即在这images里面根据角色名字创建文件夹
                #加if条件判断，文件夹不存在才创建文件夹，利用os.path.exists()方法
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                for index,image_url in enumerate(image_urls):
                    #添加字典到队列即中间者，方便消费者提取url和知道存储的位置
                    # 由于dir_path只是知道了如猪八戒等的文件夹名，还需补充xx.jpg
                    #故前面的for循环调用enumerate()方法获取下标
                    #然后再利用os.path.join()进行路径拼接，实现images/猪八戒/xx.jpg
                    self.image_queue.put({"image_url":image_url,"image_path":os.path.join(dir_path,"%d.jpg"%(index+1))})


"""消费者，下载壁纸"""
class Consumer(threading.Thread):
    def __init__(self,image_queue,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.image_queue = image_queue

    def run(self) -> None:
        #前面由于是从网络获取生产数据，可能来不及生产，所以不能直接用判断image_queue是否为空
        #get()方法没有数据会堵塞等待数据，可以用while True条件
        while True:
            #因为之前image_queue传入的是字典，所以定义变量提取字典对象
            #达到从中间者获取数据给消费者
            #get()设置timeout时间参数，当超过时间get()会报错，而不是堵塞
            #报错说明这个时间10s内没有数据即爬完了，这时候可以俘获异常处理成break
            try:
                image_dic = self.image_queue.get(timeout = 10) #单位为秒
                #提取字典的图片url
                image_url = image_dic['image_url']
                #读取字典的图片存储路径
                image_path = image_dic['image_path']
                #由于图片下载过程中有可能出现异常,所以加个try-except俘获异常
                try:
                    #利用urllib的request模块的urlretrieve()下载图片
                    request.urlretrieve(image_url,image_path)
                    #打印下载完成标志
                    print(image_path+'此图片下载完成!')
                except:
                    print(image_path+"此图片下载失败!!")

            except:
                print('搞定!!!')
                break

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
    #创建url队列(fifo)(先进先出)
    page_queue = Queue(22)
    image_queue = Queue(2000)
    #给定爬取10页(全部有22页)的url,且下标是从0开始
    for x in range(0,11):
        page_url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={}&iOrder=0&iSortNumClose=1&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1595339742487'.format(x)
        #添加url到队列
        page_queue.put(page_url)
    #创建3个生产者线程(用于获取url)
    for x in range(3):
        th = Producer(page_queue,image_queue,name = '生产者%d号'%x)
        th.start()
    #创建6个消费者线程(用于下载)
    for x in range(6):
        th = Consumer(image_queue,name = '消费者%d号'%x)
        th.start()


if __name__ == '__main__':
    main()