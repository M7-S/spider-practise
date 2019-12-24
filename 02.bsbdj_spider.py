# coding=utf-8
import requests
import re
import json

class bs_spider():
    def __init__(self):
        self.url = "http://www.budejie.com/detail-{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Referrer Policy": "no - referrer - when - downgrade",
            "Cookie": "_ga=GA1.2.934512077.1575205598; _gid=GA1.2.607685660.1577191441; BAIDU_SSP_lcr=https://www.baidu.com/link?url=R7TE7D-qq4vwWrIuT_gI-GDDEb1ZgckAUHjKFDZUG7BgPmIAEihLkdW_Csa5vNZq&wd=&eqid=b067a86300175207000000025e0220c9; Hm_lvt_7c9f93d0379a9a7eb9fb60319911385f=1575205598,1577191441,1577197773; Hm_lpvt_7c9f93d0379a9a7eb9fb60319911385f=1577203547"
        }

    def parse_url(self, url):#获取响应
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):#正则匹配段子和下一页URL
        content_list = re.findall(r"<h1>(.*?)</h1>", html_str, re.S)
        next_url = re.findall(r"data-id\=\"(.*?)\">下一条", html_str)
        #class ="c-next-btn" href="/detail-29835552.html" data-id="29835552" > 下一条 < / a >
        #data - id = "29835552" > 下一条 < / a >
        #print(html_str)
        #print(content_list)
        #print(next_url[0])
        return content_list, next_url

    def save_duanzi(self, content_list, url_num):#保存第一页内容
        with open("百思不得姐段子.txt", "a", ) as f:
            f.write(self.url.format(url_num)+"\n"+json.dumps(content_list[0],ensure_ascii=False))
            f.write("\n")
        print(self.url.format(url_num), "保存成功")

    def save_duanzi2(self, content_list, next_num):#保存第二页内容
        with open("百思不得姐段子.txt", "a", ) as f:

            f.write(self.url.format(next_num[0])+"\n"+json.dumps(content_list[0],ensure_ascii=False))
            f.write("\n")
        print(self.url.format(next_num[0]), "保存成功")


    def run(self):
        # 1. start_url
        url_num = 29961244
        # 2. 发送请求，获取响应
        html_str = self.parse_url(self.url.format(url_num))
        #print(html_str.content.decode())
        # 3. 提取数据
        content_list, next_num = self.get_content_list(html_str)
        # 4. 保存
        self.save_duanzi(content_list, url_num)
        # 5. 构造循环
        while True:
            html_str2 = self.parse_url(self.url.format(next_num[0]))
            # 3. 提取数据
            content_list2, next_num = self.get_content_list(html_str2)
            # 4. 保存
            self.save_duanzi2(content_list2, next_num)


if __name__ == '__main__':
    spider = bs_spider()
    spider.run()
