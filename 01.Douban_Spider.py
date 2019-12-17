"先测试"

"""import requests

headers = {
    "Referer": "https://m.douban.com/tv/american",
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36"}
url = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?os=android&for_mobile=1&callback=jsonp1&start=0&count=18&loc_id=108288&_=0"
response = requests.get(url, headers=headers)
#with open("11.json", "w", encoding="utf-8") as f:
 #   f.write(response.str())
print(response)"""

# coding=utf-8

import requests
import json


class Douban_spider:
    def __init__(self):
        self.start_url = "https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?os=android&for_mobile=1&callback=jsonp2&start={}&count=18&loc_id=108288&_=0"
        self.headers = {
            "Referer": "https://m.douban.com/tv/american",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36"}

    def parse_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url)
        return response.content.decode()

    def get_content_list(self, json_str):  # 提取数据
        dict_ret = json.loads(json_str)
        content_list = dict_ret["subject_collection_items"]
        # print("提取完成")
        return content_list

    def save_content_list(self, content_list):  # 保存
        with open("douban.txt", "a", encoding="utf-8-sig", errors='ignore') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")  # 写入换行符
            print("保存完成")

    def run(self):  # 实现主要逻辑

        # 1 start_url
        num = 0

        while num < 100:
            url = self.start_url.format(num)
            # 2 发送请求，获取响应
            json_str = self.parse_url(url)
            # 3 提取数据
            content_list = self.get_content_list(json_str)
            # 4 保存
            self.save_content_list(content_list)
            # 5 构造下一个url地址
            num += 18


if __name__ == '__main__':
    douban_spider = Douban_spider()
    douban_spider.run()
