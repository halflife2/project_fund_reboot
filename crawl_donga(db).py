""" 동아일보 특정 키워드를 포함하는, 특정 날짜 이전 기사 내용 크롤러(정확도순 검색)
    python [모듈 이름] [키워드] [가져올 페이지 숫자] [결과 파일명]
    한 페이지에 기사 15개
"""

from __future__ import print_function
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from lexrankr import LexRank
from konlpy.tag import Twitter
import re
import MySQLdb
from yahoo_finance import Share

TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_REST = '&check_news=1&more=1&sorting=1&search_date=1&v1=&v2=&range=3'

def html2text(html):
    soup = BeautifulSoup(html)
    text_parts = soup.findAll(text=True)
    return ''.join(text_parts)

def get_link_from_news_title(page_num, URL, code):
    for i in range(page_num):
        current_page_num = 1 + i * 15
        position = URL.index('=')
        URL_with_page_num = URL[: position + 1] + str(current_page_num) \
                            + URL[position + 1:]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        out = []
        print(URL)
        for title in soup.find_all('p', 'tit'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']

            get_text(article_URL, code)




# 기사 본문 내용 긁어오기 (위 함수 내부에서 기사 본문 주소 받아 사용되는 함수)
def get_text(URL, code):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    date = soup.select('span.date01')

    print(html2text(str(date[1])))

    out = []
    for item in content_of_article:
        [item.extract() for item in soup('script')]
        [item.extract() for item in soup('div')]

        string_item = item.find_all(text=True)
        #lexranker(str(string_item), code, date)



# lexrank함수 (문장 요약)
def lexranker(text,code,date):

    text = text.replace('\\n','.')
    text2 = re.sub('[^가-힝0-9a-zA-Z\\s\\.]', '', text)

    lexrank =LexRank()
    #print(text2)
    lexrank.summarize(text2)
    summaries = lexrank.probe(3)
    word = Twitter()
    out = []
    print(summaries)
    for summary in summaries:
        out += word.nouns(summary)

    word = list(set(out))
    share = Share(code)
    startprice = share.get_open()
    endprice = share.get_price()
    for part in word:
        save_record(part, code, startprice, endprice, date)


####################### db connection ###################################
def save_record(word, code, startprice, endprice, date):
    #open database connection
    db = MySQLdb.connect("ghjuy.iptime.org","webuser","abcd1234","WordDB" )

    db.set_character_set('utf8')

    cursor = db.cursor()

    sql = "INSERT INTO word_table(word, code, start_price, end_price, date) values(N\'"+word+"\',\""+code+"\",\""+startprice+"\",\""+endprice+"\",\""+date+"\")"

    try:
        #Excute the SQL command
        cursor.execute("set names utf8")

        cursor.execute(sql)

        #commit changes in the database
        db.commit()

        #cursor.execute("""SELECT col1 FROM WordDB.word_table""")
        #print(cursor.fetchall())
    except Exception as e:
        print(str(e))
        #Rollback in case there is any error
        db.rollback()

    #Disconnect from database
    db.close()



# 메인함수
def main(argv):
    if len(argv) != 3:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    code = '005930.KS'
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEWORD \
                 + quote(keyword) + TARGET_URL_REST
    get_link_from_news_title(page_num, target_URL, code)




    #print(word[13])


if __name__ == '__main__':
    main(sys.argv)

