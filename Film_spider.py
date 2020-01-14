# coding=utf-8
# 爬取地址https://www.dytt8.net/html/gndy/dyzz/list_23_1.html
import requests,re
from lxml import etree
import time
import random


class FilmSpider():
    def __init__(self):
        self.url = "https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
        self.film_url = "https://www.dytt8.net{}"
        #self.headers = {
        #    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        #    "Referrer Policy": "no - referrer - when - downgrade"
        #}
        USER_AGENTS = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        ]

        self.headers = {"User-Agent": random.choice(USER_AGENTS)}


    def parse_url(self, url):
        response = requests.get(url, headers=self.headers).content.decode(encoding='gbk', errors='ignore')
        response=etree.HTML(response)
        return response

    def parse_film_url(self,url):
        response = requests.get(url, headers=self.headers).content.decode(encoding='gbk', errors='ignore')
        return response

    def get_content_list(self,html_str):#用xpath选取电影名称和电影链接，并构造出电影名称-电影链接字典
        item_name_list = html_str.xpath("//b/a/text()")
        item_url_list =html_str.xpath("//b/a/@href")
        item_name_url = zip(item_name_list, item_url_list)
        name_url_dict = dict((key, value) for key, value in item_name_url)
        return name_url_dict

    def get_filmdownload_url(self,html_download_str):
        m = re.findall(r"(magnet\:.*?)\"\>",html_download_str,re.S)
        return m

    def film_save(self,key,val):#保存电影名称和下载链接
        with open("电影链接下载.txt", "a", ) as f:
            f.write(key+"\n")
            f.write(val[0] + "\n")
        print(key+"保存成功")


    def run(self):
        # 1构造电影列表
        i = 4
        while i <= 207:
            url = self.url.format(i)
            html_str = self.parse_url(url)
            #构造电影名称列表和地址列表
            film_name_url = self.get_content_list(html_str)
            for key,value in film_name_url.items():
                film_url=self.film_url.format(value)
                html_download_str = self.parse_film_url(film_url)
                val= self.get_filmdownload_url(html_download_str)
                #print(val)
                if len(val):
                    self.film_save(key,val)
                else:
                    pass
                #time.sleep(0)
            i+=1

if __name__ == '__main__':
    film=FilmSpider()
    film.run()


