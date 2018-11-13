"""뉴스 기사 웹 크롤러 모듈"""

from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen
from urllib.request import HTTPError
import urllib.request
import re
import sys
import datetime



#출력파일명

#긁어올 url
URL1 = 'http://vip.mk.co.kr/newSt/news/news_view.php?p_page=&sCode=21&t_uid=20&c_uid='
URL2 =  '&search=&topGubun='
news_num = 1494497
complete_URL = URL1 + str(news_num) + URL2


#url 2
URL3 = 'http://file.mk.co.kr/news/rss/rss_30000001.xml'

#변수들


news = [

           [  ],                    #web 주소
           [ [],[],[],[],[],[] ],   #제목 6단어(띄어쓰기로 구분)
           [ [],[],[],[] ]          #날짜 (연.월.일.시간)
                                    ]


#뉴스 제목 크롤링

def get_title(URL3,OUTPUT_FILE_NAME,thing):


    tt = open(OUTPUT_FILE_NAME, 'w')
    tt.close()

    req = urllib.request.Request(URL3)
    data = urllib.request.urlopen(req)
    soup = BeautifulSoup(data, 'html.parser',from_encoding='utp-8')

    tag_finder = soup.find_all(thing)
    #time_finder = soup.fina_all('td' , class = "t_11_brown")
    idx=0

    for s in tag_finder:
        try:
            tt = open(OUTPUT_FILE_NAME, 'a')
            title = "%s \n" % (str(s))
            title = clean_text(title)
            tt.write(title)
        except UnicodeEncoderError:
            tt = open(OUTPUT_FILE_NAME, 'a')
            error_num = "Error : %d \n" % (idx)
            tt.write(error_num)
        finally:
            idx += 1

#클린함수없는 get_title
def noclean_get_title(URL3,OUTPUT_FILE_NAME,thing):

    tt = open(OUTPUT_FILE_NAME, 'w')
    tt.close()

    req = urllib.request.Request(URL3)
    data = urllib.request.urlopen(req)
    soup = BeautifulSoup(data, 'html.parser',from_encoding='utp-8')

    tag_finder = soup.find_all(thing)
    #time_finder = soup.fina_all('td' , class = "t_11_brown")
    idx=0

    for s in tag_finder:
        try:
            tt = open(OUTPUT_FILE_NAME, 'a')
            title = "%s \n" % (str(s))
            tt.write(title)
        except UnicodeEncoderError:
            tt = open(OUTPUT_FILE_NAME, 'a')
            error_num = "Error : %d \n" % (idx)
            tt.write(error_num)
        finally:
            idx += 1



#파일 읽기

def read_text(OUTPUT_FILE_NAME):

    read_file = open(OUTPUT_FILE_NAME, 'r')

    for i in range(2,50):

        text = read_file.readline()
        news[0] = text[15:68]
        print(news[0])
        #tt=open('read_link.txt', 'a')
        #tt.write(news[0])

    #tt.close()







# 크롤링 함수

def get_text(complete_URL):
    global news_num

    source_code_from_URL = urllib.request.urlopen(complete_URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('div', id='Conts'):
        text = text + str(item.find_all(text=True))

    return text



# 클리닝 함수
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*`!^\-_+<>@\#$%&\\\=\(\'\"■◆]',
                          '', cleaned_text)
    return cleaned_text
   # 클리닝함수 지울부분



# 메인 함수
def main():

    #연속 쓰기
     get_title(URL3,'output.txt','description')

     noclean_get_title(URL3,'output_link.txt','link')
     read_text('output_link.txt')

     noclean_get_title(URL3,'output_time.txt','pubDate')

     #print(now)









if __name__ == '__main__':
    main()
