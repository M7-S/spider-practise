# coding=utf-8
import requests,re

class konachan_spider():
    def __init__(self):
        self.url = "http://konachan.net/post?page={}&tags="
        self.pic_url ="http://konachan.net/post/show/{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

    def parse_url(self, url):#获取响应
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_content_list(self, html_str):#正则匹配段子和下一页URL
        content_list = re.findall(r"\"\/post\/show\/(.*?)\"", html_str,)
        return content_list

    def get_picture_url(self,pic_url_str):#正则匹配图片高清网页
        picture_url = re.findall(r"changed\"\shref\=\"(.*?)\"", pic_url_str)
        return picture_url[0]

    def save_pic(self,content,pic_url_str):
        pic_name =content.replace("/","_") + ".jpg"
        with open(pic_name, 'wb') as f:
            f.write(pic_url_str)

    def run(self):  # 主程序
        # 1 构造列表页URL
        i = 1
        while True:
            url = self.url.format(i)
            # 2 列表页发送请求，获取响应
            html_str = self.parse_url(url).decode()
            # 3 提取图纸链接数据
            content_list = self.get_content_list(html_str)
            #print(content_list)
            for content in content_list:
                print(content)
                pic_url = self.pic_url.format(content)
                #print("pic_url="+ pic_url)
                # 4 提取壁纸原画质页面
                pic_url_str = self.parse_url(pic_url).decode()
                #print(pic_url_str)
                picture_url =self.get_picture_url(pic_url_str)
                #print(picture_url)
                picture_content = self.parse_url(picture_url)
                # 5 保存壁纸
                self.save_pic(content,picture_content)
                print("下载成功")
                # 6 循环遍历
                i+=1

if __name__ == '__main__':
    konachan_spider().run()
