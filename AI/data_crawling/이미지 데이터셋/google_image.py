from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

if not os.path.isdir("소묘/"):
    os.makedirs("소묘/")

chrome_driver = "C:\\Users\\HP\\PycharmProjects\\final_project\\chromedriver.exe"

URL = "https://www.google.co.kr/imghp?hl=ko&ogbl"


# 크롬 드라이버 세팅
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
# 페이지 열기
driver.get(URL)

search = "뎃생"
elem = driver.find_element(By.NAME, "q")
elem.send_keys(search)
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR,".mye4qd").click()
        except:
            break
    last_height = new_height
    time.sleep(2)
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    count = 1

for image in images:
    try:
        image.click()
        time.sleep(2)

        imgUrl = driver.find_element(By.XPATH, "//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img").get_attribute('src')
        urllib.request.urlretrieve(imgUrl, "뎃생/" + search + "_" + str(count) + ".jpg")
        print("Image saved: 뎃생_{}.jpg".format(count))
        count += 1
    except:
        pass

driver.close()