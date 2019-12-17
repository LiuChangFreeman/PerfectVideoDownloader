# perfect_video_downloader
腾讯视频、优酷、爱奇艺视频下载器，满速、无水印 
## 说明
本项目基于由[N_m3u8DL-CLI](https://nilaoda.github.io/N_m3u8DL-CLI/)提供的m3u8下载器，[下载地址](http://static.aikatsucn.cn/static/perfect_video_downloader.zip)  
## 必要条件
1. Windows
2. Python
3. Chrome浏览器
## 安装步骤
1、解压**perfect_video_downloader.zip**到任意文件夹  
2、运行pip命令安装必要的库
``` bash
pip install -r requirements.txt
```
3、填写必要信息
``` python
# chrome浏览器路径
chrome_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
#视频保存的路径
path_to_save=r"C:\videos"
# 线程数
threads=64
# chrome使用的端口
port_chrome=9224

# 待下载的剧集
url_videos=[
  {
      "title": "庆余年: 第1集", "url": "https://www.iqiyi.com/v_19ruzj8gv0.html"
  }
]
```
4、在Chrome中登录您的会员账号(爱奇艺、腾讯、优酷)  
5、在**命令行**中运行脚本
```
python main.py
```