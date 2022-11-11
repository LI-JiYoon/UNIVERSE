# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json


client_id = "Oojdb1BJkP_jR6Ubdc6V"
client_secret = "WWUnvX7rY3"

encText = urllib.parse.quote("일러스트")
start = 1

while start < 1000 :
    url = "https://openapi.naver.com/v1/search/image?query=" +  encText + "&display=100&start=" + str(start) # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    # rescode:
    # 통신 오류--- 누가 잘 못했나. 너 아님 나겠지
    # 데이터 받는 쪽에서 log를 확인해야 한다
    # 보통 백엔드 쪽에서 log 확인을 해주는게 일반적
    # json 파일 파싱시 어떻게 접근해야하나
    # restapi를 만들게 되면 프로토콜 통신이 가능한 문서를 만들어 주는데
    # 이 문서를 파싱을 해야하는데 파싱을 하려면어떻게 해야되는가.
    #1. import json
    #
    # 기본적으로 json은 key-value 형태로 들어간다
    # google에 json parser 라고 검색을 한다. http://json.parser.online.fr/
    #그러면 json 파일을 좀더 예쁘게 보여 준다
    if(rescode==200):
        response_body = response.read()
        response_body = json.loads(response_body) # 위에 받은 response-body를 json 형식으로 파싱할 수 있도록 .load 해 줍니다.

        #print("items 개수: " ,len(response_body['items'])) # items 키값의 value 개수 출력

        for item in response_body['items']:  # 주소(item 안의 link란 키의 value 값) 저장
           link = item['link']
           link_parser = link.split('/')
           savename = link_parser[-1]

           try:
            urllib.request.urlretrieve(link, './디지털페인팅/' + savename)
           except:
               print('error : ' , savename )
            # 7개의 이미지 save

        #print(response_body.decode('utf-8'))--josn 파일 확인
    else:
        print("Error Code:" + rescode)
    start += 100
    
# 네이버블로그 스크래핑
# m. + 블로그 주소 (모바일 버전으로 가져옴)
# beautifulsoup 으로 계속 접속해서 원하는 텍스트만 가져옴 --- naver mobile 은 보안이그다지 철저하지 않음
# 네이버 카페의 경우 1, 모바일 버전 2. 네이버 카페 하단의 페이지 주소로 접근하여 가져온다