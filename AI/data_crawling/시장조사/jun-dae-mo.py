#전대모

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

chrome_driver = "C:\\Users\\HP\\PycharmProjects\\final_project\\chromedriver.exe" # 파일 확장자 이름 표기
#chrome_driver = '../chromedriver' # 파일 확장자 이름 미표기

URL = 'https://nid.naver.com/nidlogin.login'
id = 'ljy99126'
pw = 'in67072654'

# 크롬 드라이버 세팅
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(chrome_driver, options=chrome_options)
# 페이지 열기
driver.get(URL)
# 페이지 로딩 대기
driver.implicitly_wait(2)

elem_id = driver.find_element(By.NAME, "id")
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')  # ID 입력
time.sleep(1)


elem_pw = driver.find_element(By.NAME, 'pw')
elem_pw.click()
pyperclip.copy(pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)


# 로그인 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="log.login"]').click()
time.sleep(1)

qnaboard_url = "https://cafe.naver.com/ArticleList.nhn?search.clubid=10797658&search.menuid=561&userDisplay=50&search.boardtype=L&search.specialmenutype=&search.totalCount=501&search.cafeId=10797658&search.page="

# 게시글을 50개씩 가져오는 것으로 설정함
# nth-child(n) 에서 n 은 해당 페이지의 50개의 글 중 n번째임을 뜻함


baseurl = qnaboard_url
second_url = "https://cafe.naver.com"
link_list = []
dataset = []
content_dataset = []

# #첫페이지 공지글 제거
# driver.get(baseurl+str(1))
# time.sleep(1)
# #
# #
# driver.switch_to.frame('cafe_main')
# #
# html = driver.page_source
#
# soup = bs(html, 'html.parser')
# content_nums = soup.find_all(class_='inner_number') #게시클 번호 전부 가져오기
# titles = soup.find_all(class_='article') # 게시글제목
# links = soup.find_all(class_ = 'inner_list') #각 게시글 링크
# dates = soup.find_all(class_='td_date') # 게시글 게시 날찌
# views = soup.find_all(class_='td_view') # 게시들 조회수
# likes = soup.find_all(class_ = 'td_likes') # 게시글 좋아요수
#
# for content_num, title, link, date, view, like in zip(content_nums, titles[6:], links[6:], dates[6:], views[6:], likes[6:]):
#     try:
#         cafedict = {'num': content_num.text,
#                     'title': title.text.strip(),
#                     'link': link.find("a")['href'],
#                     'view': view.text,
#                     'date': date.text,
#                     'likes': like.text}
#         print(cafedict)
#         dataset.append(cafedict)
#     except:
#         break
#
#
#     print('1 done')
#
#
#
#
# for pg_n in range(2,126): #총 페이지수:125
#     driver.get(baseurl+str(pg_n))
#     time.sleep(1)
# #
# #
#     driver.switch_to.frame('cafe_main')
# #
#     html = driver.page_source
#
#     soup = bs(html, 'html.parser')
#
#
#     content_nums = soup.find_all(class_='inner_number') #게시클 번호 전부 가져오기
#     titles = soup.find_all(class_='article') # 게시글제목
#     links = soup.find_all(class_ = 'inner_list') #각 게시글 링크
#     dates = soup.find_all(class_='td_date') # 게시글 게시 날찌
#     views = soup.find_all(class_='td_view') # 게시들 조회수
#     likes = soup.find_all(class_ = 'td_likes') # 게시글 좋아요수
#
#     for content_num, title, link, date, view, like in zip(content_nums, titles, links, dates, views, likes):
#         try:
#            cafedict = {'num': content_num.text,
#                        'title': title.text.strip(),
#                        'link': link.find("a")['href'],
#                        'view': view.text,
#                        'date': date.text,
#                        'likes': like.text}
#            print(cafedict)
#            dataset.append(cafedict)
#         except:
#             break
#
#
#     print( str(pg_n) + ' done')
#
#
# df = pd.DataFrame(dataset)
# df.to_csv('navercafe_jundaemo(schoollife_qna)dataset.csv', encoding = 'utf-8-sig') # csv 파일로 저장

df = pd.read_csv('navercafe_jundaemo(schoollife_qna)dataset.csv')

cnt = 0
for link in df['link']:
    try:
        time.sleep(1)
        driver.get(second_url + link)
        time.sleep(4)
        driver.switch_to.frame('cafe_main')

        html = driver.page_source
        soup = bs(html, 'html.parser')

        writer_div = soup.find('div', {'class' : 'WriterInfo'})
        content_div = soup.find('div', {'class' :'content CafeViewer'})
        comment_num_div = soup.find('div', {'class': 'box_left'})

        cafecontent_dict = {'writer': writer_div.find('div', {'class' : 'nick_box'}).text.strip(),
                                'content':content_div.find('div', {'class' : 'se-module se-module-text'}).text.strip(),
                                'comment_num': comment_num_div.find("strong").text}
        content_dataset.append(cafecontent_dict)

    except:
        print('삭제된 게시물입니다.')
        cafecontent_dict = {'writer': '삭제된 게시물 입니다.',
                            'content': '삭제된 게시물 입니다.',
                            'comment_num': '삭제된 게시물 입니다.'}
        content_dataset.append(cafecontent_dict)
        continue

    print(cafecontent_dict)
    cnt+=1
    print(cnt)
#
#
driver.quit()
#
#
#
df = pd.DataFrame(content_dataset)
df.to_csv('navercafe_jundaemo(schoollife_qna_content)dataset.csv', encoding = 'utf-8-sig') # csv 파일로 저장


