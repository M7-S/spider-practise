# coding=utf-8
# 爬取地址 http://konachan.net/post?page=1&tags=
import requests, re
import threading
from queue import Queue


class konachan_spider():
    def __init__(self):
        self.url = "http://konachan.net/post?page={}&tags="
        self.pic_url = "http://konachan.net/post/show/{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        self.url_queue = Queue()
        self.url_large_queue = Queue()
        #self.url_save_queue = Queue()

    def get_url_list(self):  # 构造图片URL列表
        i = 1
        while i<50:
            html_str = requests.get(self.url.format(i), headers=self.headers).content.decode()
            pic_url_list = []
            content_list = re.findall(r"\"\/post\/show\/(.*?)\"", html_str)
            for content in content_list:
                pic_url_list.append(self.pic_url.format(content))
            # return pic_url_list, len(content_list)
            num = len(content_list)
            for n in range(0, num):
                self.url_queue.put(pic_url_list[n])

    def get_larger_version_list(self):  # 构造高清图URL列表
        while True:
            pic_url= self.url_queue.get()
            html_str = requests.get(pic_url, headers=self.headers).content.decode()
            picture_url = re.findall(r"changed\"\shref\=\"(.*?)\"", html_str)
            # print(picture_url[0])
            #return picture_url[0]
            self.url_large_queue.put(picture_url[0])
            self.url_queue.task_done()

    def save_pic(self):  # 保存图片文件
        while True:
            url = self.url_large_queue.get()
            pic_url_str = requests.get(url, headers=self.headers).content
            pic_name = url.replace("/", "_") + ".jpg"
            with open(pic_name, 'wb') as f:
                f.write(pic_url_str)
            self.url_large_queue.task_done()

    def run(self):
        thread_list = []

        t1_url=threading.Thread(target=self.get_url_list)
        thread_list.append(t1_url)
        t1_large_url = threading.Thread(target=self.get_larger_version_list)
        thread_list.append(t1_large_url)

        t1_save = threading.Thread(target=self.save_pic)
        thread_list.append(t1_save)
        for t in thread_list:
            t.start()



if __name__ == '__main__':
    konachan_spider().run()