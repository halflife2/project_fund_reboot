import ssl
import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_conditions
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


driver = webdriver.Firefox(executable_path='/Users/ItsFriday/Documents/GitHub/project_fund/geckodriver')
driver.implicitly_wait(30)
driver.get('https://kr.investing.com/stock-screener/?sp=country::11|sector::a|industry::a|equityType::a%3Ceq_market_cap;1')

box = driver.find_elements_by_xpath("//table[@id='resultsTable']/tbody/tr")
for item in box:
    data = item.text
    print(data, '\n')
# for i in box:
#     print(i, '\n')

#listed_box = [item.text for item in enumerate(box) if item != 0]
# for item in box:
#     print(item.text)
