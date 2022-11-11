import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service # selenium 사용시 기본 import 패키지
from bs4 import BeautifulSoup



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()),options= chrome_options )
# 크롬 브라우저를 띄우는 코드


driver.maximize_window()
# 창을 크게하고
time.sleep(2) # 잠깐 텀을 두고
driver.get('https://yandex.com/images/search?text=oil%20painting&lr=10635') # 웹페이지 주소
time.sleep(3)


body = driver.find_element(By.CSS_SELECTOR, 'body') #웹페이지의 html 파일 에서 body 선택
for tem in range(5):
    body.send_keys(Keys.PAGE_DOWN) # pagedowm 키를 5번 누릅니다
    time.sleep(1)

html = driver.page_source # 해당 ㅠ파일 가져오고

bs = BeautifulSoup(html,'html.parser') # 위의 html 웹페이지를 html.parser 로 파싱합니다.

result = bs.find_all('div', class_ = 'serp-item') #class_ 인 이유는 그냥 class는 예약어이기 떄문

for temp in result: # temp에는 태그 시작부터 끝까지가 들어있음.
    print(temp['data-bem']) # data-bem 태그만 가져옴


