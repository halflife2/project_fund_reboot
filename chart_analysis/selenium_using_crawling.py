import ssl
import sys
import io
from selenium import webdriver


ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

exe_path = '/Users/ItsFriday/Documents/GitHub/project_fund/geckodriver'
driver = webdriver.Firefox(executable_path=exe_path)
driver.implicitly_wait(30)

for i in range(1, 46):
    URL = 'https://kr.investing.com/stock-screener/?sp=country::11|sector::a|industry::a|equityType::a%3Ceq_market_cap;' + str(i)
    driver.get(URL)

    xpath = "//table[@id='resultsTable']/tbody"
    element = driver.find_element_by_xpath(xpath)
    elements = [item.get_attribute('href') for item in element.find_elements_by_css_selector('a')]

    with open('total_url.txt', 'at') as f:
        for item in elements:
            f.write(item + '\n')
