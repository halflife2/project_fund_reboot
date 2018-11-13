""" 동아일보 특정 키워드를 포함하는, 특정 날짜 이전 기사 내용 크롤러(정확도순 검색)
    python [모듈 이름] [키워드] [가져올 페이지 숫자] [결과 파일명]
    한 페이지에 기사 15개
"""

import sys
from bs4 import BeautifulSoup
import urllib.request
import requests
from urllib.parse import quote


TARGET_URL_BEFORE_PAGE_NUM = "https://search.naver.com/search.naver?start="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&ie=utf8&where=news&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=1&ds=2017.05.03&de=2017.05.10&docid=&nso=so:r,p:1w,a:all&mynews=0&cluster_rank=129&refresh_start=0'


def get_link_from_news_title(url,page_num,output_file):
    for i in range(page_num):
        current_page_num = 1 + i * 10
        position = url.index('=')
        URL_with_page_num = url[: position + 1] + str(current_page_num) \
                            + url[position + 1:]
        print(URL_with_page_num)

        source_code = requests.get(URL_with_page_num)
        text_f=source_code.text
        soup=BeautifulSoup(text_f,'lxml')
        for title_list in soup.find_all("a",{"class":"_sp_each_url"}):
            
            
            if title_list.get('href')[0:22]=="http://news.naver.com/":
                href=title_list.get('href')
                #print(href) 실행창에 각 기사의 링크 출력
                get_text(href, output_file)

# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml')
    text=''
    content_of_article = soup.find_all('div', id='articleBodyContents')
    for item in content_of_article:
        text = text+str(item.find_all(text=True))
        #print(text) 실행창에 크롤링 본문 출력
        try: #인코딩 예외처리
            output_file.write(text)
        except:
            continue


def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] [결과 파일명]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    output_file_name = argv[3]

    url = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD + \
                 quote(keyword) + TARGET_URL_REST
    print(url) # 페이지 숫자 제외 url 출력

    output_file = open(output_file_name, 'w')
    get_link_from_news_title(url,page_num,output_file)
    output_file.close()

if __name__ == '__main__':
    main(sys.argv)
