import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import os
import urllib.request
import re
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_driver = "C:\\Users\\HP\\PycharmProjects\\final_project\\chromedriver.exe"

watercolor_URL = 'https://stock.adobe.com/kr/search/images?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k=watercolor+painting&order=relevance&safe_search=1&search_page='
watercolor_URL_second ='&search_type=usertyped&acp=&aco=watercolor+painting&get_facets=1'
oil_paint_URL = 'https://stock.adobe.com/kr/search/images?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k=Oil+painting&order=relevance&safe_search=1&search_page='
oil_paint_URL_second = '&search_type=usertyped&acp=&aco=Oil+painting&get_facets=1'
# 크롬 드라이버 세팅
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

img_url_list = []

for x in range(1, 101):
    url = oil_paint_URL + str(x) + oil_paint_URL_second
    # 페이지 열기
    driver.get(url)
    # 페이지 로딩 대기
    time.sleep(5)
    # search-results > div:nth-child(1) > div.thumb-frame > a > picture > img
    # search-results > div:nth-child(1) > div.thumb-frame > a > picture > img
    html = driver.page_source
    soup = bs(html, 'html.parser')
    tags = soup.select('picture > img')#['src']#, {'src'})#:re.compile('\.\.\/img\/gifts/img.*\.jpg'
    for tag in tags:
        image = tag.get('data-lazy')
        if image == None:
            continue
        img_url_list.append(image)

    print('page' + f'{x}' + 'done')
    #for image in images:
    #    img_url = image.get_attribute('src')
    #    img_url_list.append(img_url)

    # print(img_url)



img_folder = '.\\oilpaint'
#img_folder = '.\\watercolorpaint'

if not os.path.isdir(img_folder):  # 없으면 새로 생성하는 조건문
    os.mkdir(img_folder)

for index, link in enumerate(img_url_list):
    print(link)
    #     start = link.rfind('.')
    #     end = link.rfind('&')
    #     filetype = link[start:end]
    urllib.request.urlretrieve(link, f'./oilpaint/{index}.jpg')