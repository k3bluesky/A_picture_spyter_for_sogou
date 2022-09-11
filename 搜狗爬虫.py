import requests
import re
import os
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400QQBrowser/10.5.3863.400',

}  # 请求头


def spider(img_name, img_num):
    n = 1
    p = 1
    dir_name = img_name  # 生成文件夹
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    time.sleep(2)
    while p <= img_num:
        page = p * 48 #一页48张图片

        url = 'https://pic.sogou.com/napi/pc/searchList?mode=1&start={}&xml_len=48&query={}'.format(page,img_name)
        if(img_num>=1):p+=1
        response = requests.get(url, headers=headers)
        plt = re.findall(r'\"picUrl\"\:\".*?\"', response.text)  # response.text是以unicode返回响应的内容
        print(plt)
        for i in plt:
            pic_url = i.split(':')[2][0:-1]
            pic_name = dir_name + '/' + str(n) + '.jpg'
            pic_url = re.sub(r'\\u002F', '/', pic_url)
            if(pic_url[-4:] != '.jpg' and pic_url[-4:] != '.png' and pic_url[-5:] != '.jpeg'):continue
            try:
                result_pic = requests.get('http:' + pic_url, headers=headers)
            except:
                continue
            # 存入文件，注意使用二进制存储(wb+),b是二进制存储，所有多媒体(图片、音乐、视频)文件都是二进制
            with open(pic_name, 'wb+') as f:
                f.write(result_pic.content)
            print(pic_name + "downloading........")
            n += 1
    print('end', "success!")


if __name__ == '__main__':
    name = input("please input keywords:")
    page = input("please input page:")
    spider(name, page)  # 关键词在这里修改

