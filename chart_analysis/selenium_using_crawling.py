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

xpath = "//table[@id='resultsTable']/tbody"
element = driver.find_element_by_xpath(xpath)
elements = [item.get_attribute('href') for item in element.find_elements_by_css_selector('a')]
for item in elements:
    print(item)
