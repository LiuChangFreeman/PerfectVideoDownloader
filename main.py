# -*- coding: utf-8 -*-
from __future__ import print_function
from sys import version_info
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import win32process
import os
import re
import json
import requests
from bs4 import BeautifulSoup
import time

chrome=None

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
        "title": "庆余年: 第14集", "url": "https://www.iqiyi.com/v_19rurcgqzs.html"
    }
]

def launch_chrome():
    global chrome
    if os.path.exists(chrome_path):
        command="\"{}\"--remote-debugging-port={}".format(chrome_path, port_chrome)
        print(u"如果Chrome白屏，请使用CMD手动运行以下命令:\n{}".format(command))
        chrome = win32process.CreateProcess(None, "{} --remote-debugging-port={}".format(chrome_path, port_chrome),None, None, 0, 0, None, None, win32process.STARTUPINFO())
    else:
        print(u"未找到Chrome安装目录")
        exit(-1)

def main():
    # 启动chrome,如果启动失败，请删掉这一行并手动启动chrome
    launch_chrome()

    # 连接chrome
    print(u"正在试图连接到Chrome")
    chrome_options = Options()
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:{}'.format(port_chrome))
    if version_info.major == 2:
        command = u"N_m3u8DL-CLI \"{}\" --workDir \"{}\" --saveName \"{}\" --maxThreads {} --minThreads {} --enableDelAfterDone --disableDateInfo --stopSpeed 1024 --noProxy"
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        command = r"N_m3u8DL-CLI \"{}\" --workDir \"{}\" --saveName \"{}\" --maxThreads {} --minThreads {} --enableDelAfterDone --disableDateInfo --stopSpeed 1024 --noProxy"
        driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)

    # 下载剧集
    for item in url_videos:
        url=item["url"]
        title=item["title"]
        title = re.sub(r"[/\\:*?\"<>|]", "",title)
        if version_info.major == 2:
            title = title.decode("utf-8")
        try:
            driver.get(url)
            if "youku" in url:
                url_download=driver.execute_script("return videoPlayer.getData()._playlistData.stream[0].m3u8_url;")
            elif "qq" in url:
                fail_count = 0
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                labels = soup.select(".txp_label")
                resolution = labels[0].text
                if resolution != u"蓝光":
                    print(u"正在切换至最高画质")
                    menu = driver.find_element_by_class_name("txp_popup_content")
                    items = menu.find_elements_by_class_name("txp_menuitem")
                    for item in items:
                        data = item.get_attribute("data-definition")
                        if data == "fhd":
                            print(u"点击切换")
                            driver.execute_script("arguments[0].click();", item)
                            time.sleep(1)
                            break
                    while True:
                        if fail_count > 3:
                            print(u"放弃切换分辨率")
                            break
                        html = driver.page_source
                        if u"正在为您切换清晰度" in html:
                            print(u"正在切换")
                            time.sleep(1)
                        elif u"已成功为您切换清晰度" in html:
                            print(u"切换成功")
                            break
                        else:
                            print(u"切换失败")
                            fail_count += 1
                            time.sleep(1)
                url_download = driver.execute_script("return PLAYER._DownloadMonitor.context.dataset.currentVideoUrl;")
            elif "iqiyi" in url:
                url_download=os.path.join(os.path.abspath(os.path.curdir),u"{}.m3u8".format(title))
                script_iqiyi = open("iqiyi.js").read()
                driver.execute_script(script_iqiyi)
                dash_url=driver.execute_script("return window.dashUrl;")
                print(dash_url)
                cookies = driver.get_cookies()
                cookie = ""
                for item in cookies:
                    cookie += "{}={}; ".format(item["name"], item["value"])
                headers={}
                headers["Host"]="cache.video.iqiyi.com"
                headers["Connection"]="keep-alive"
                headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
                headers["Accept"]="*/*"
                headers["Sec-Fetch-Site"]="same-site"
                headers["Sec-Fetch-Mode"]="no-cors"
                headers["Referer"]="https://www.iqiyi.com/v_19rurcgqzs.html"
                headers["Accept-Encoding"]="gzip, deflate, br"
                headers["Accept-Language"]="zh-CN,zh;q=0.9"
                headers["Cookie"]=cookie
                response=requests.get(dash_url,headers=headers,timeout=15)
                result=response.text
                data = re.findall("{\".*\"}", result, re.DOTALL)
                data = json.loads(data[0])
                videos = data["data"]["program"]["video"]
                for video in videos:
                    if video["_selected"]:
                        m3u8 = video["m3u8"]
                        with open(url_download,"w") as fd:
                            fd.write(m3u8)
                        break
            else:
                continue
            print(u"已获取到m3u8地址:\n{}\n".format(url_download))
            command =command.format(url_download,path_to_save,title,threads,threads)
            if version_info.major == 2:
                command=command.encode("gbk")
            else:
                command=command.replace("\\\"","\"")
            os.system(command)
            if os.path.exists(url_download):
                os.remove(url_download)
        except Exception as e:
            print(u"发生异常:")
            print(e)

    # 退出chrome
    try:
        print(u"正在关闭Chrome进程")
        driver.quit()
        win32process.TerminateProcess(chrome[0], 0)
        os.system("taskkill /IM software_reporter_tool.exe /F")
    except:
        pass
    print(u"按任意键退出")
    if version_info.major == 2:
        raw_input()
    else:
        input()

if __name__=="__main__":
    main()
