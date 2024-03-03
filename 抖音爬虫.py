import requests  
import pandas as pd  
from bs4 import BeautifulSoup  
import os  
import  urllib3.contrib.pyopenssl
import time
import numpy
import random
requests.packages.urllib3.disable_warnings() 
urllib3.contrib.pyopenssl.inject_into_urllib3()
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES =5
s = requests.session() 
s.keep_alive = False
session = requests.session()
# 设置请求头以模拟浏览器访问  
"""headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'  
} """
headers={'Connection':'close'}
  
# 抖音热榜URL  
hot_url = 'https://www.douyin.com/hot/video'  
proxy = {'http': '33.33.33.10:8118'}  # try catch换
   
# 发送请求并获取热榜页面内容
#response = session.get(hot_url, headers={'Connection':'close'},stream=True,verify=False)
#response = requests.get(hot_url,headers={'Connection':'close'},stream=True, verify=False)
try:
	response = session.get(hot_url,headers={'Connection':'close'},proxies=proxy,stream=True, verify=False)
except:
	response = session.get(hot_url,headers={'Connection':'close'},proxies=proxy,stream=True, verify=False)
# 解析热榜页面  
soup = BeautifulSoup(response.text, 'html.parser')  
  
# 提取热榜数据  
hot_list = soup.find_all('div', class_='hot-list-item')[:50]  # 取前50条，不包括置顶  
  
# 创建DataFrame用于存储数据  
df = pd.DataFrame(columns=['排名', '标题', '链接', '时间', '热度'])  
  
for item in hot_list:  
    rank = item.find('span', class_='rank').text  
    title = item.find('a', class_='title').text  
    link = 'https://www.douyin.com' + item.find('a', class_='title')['href']  
    time = item.find('span', class_='time').text  
    heat = item.find('span', class_='heat').text if item.find('span', class_='heat') else 'N/A'  
      
    df = df.append({'排名': rank, '标题': title, '链接': link, '时间': time, '热度': heat}, ignore_index=True)  
  
# 将数据保存到Excel文件  
excel_file = 'douyin_hot_list.xlsx'  
df.to_excel(excel_file, index=False)  
print(f'热榜数据已保存到{excel_file}')  
  
# 爬取三个分区的第一个视频  
partitions = ['娱乐', '生活', '美食']  # 选择分区  
for partition in partitions:

    # 构造分区视频页的URL  
    partition_url = f'https://www.douyin.com/search_video/?search_src=1&aid=1128&_sign=3b2b76b1bb2f0518e86c52c5e6263624&keyword={partition}'  
      
    # 发送请求获取分区视频页内容  
    partition_response = requests.get(partition_url, headers=headers)  
    partition_soup = BeautifulSoup(partition_response.text, 'html.parser')  

    # 提取第一个视频的URL  
    video_link = partition_soup.find('a', class_='video-item')['href'] if partition_soup.find('a', class_='video-item') else 'N/A'  
    full_video_link = 'https://www.douyin.com' + video_link  
   
    # 发送请求获取视频数据  
    video_response = requests.get(full_video_link, headers=headers, stream=True)  
 
    # 保存视频到文件  
    video_file = f'video_{partition}.mp4'  
    with open(video_file, 'wb') as f:  
        for chunk in video_response.iter_content(chunk_size=1024):  
            if chunk:  
                f.write(chunk)  
    print(f'视频已保存到{video_file}')
time.sleep(random.random()*3+7)
