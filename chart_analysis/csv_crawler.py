import ssl
import sys
import io
import time
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

class SeleniumCrawler:
    def __init__(self):
        if platform.system() == 'Darwin':
            exe_path = '/Users/ItsFriday/Documents/GitHub/project_fund/geckodriver'
        elif platform.system() == 'Windows':
            exe_path = '/project1/project_fund_reboot/geckodriver(win64)'

        self.driver = webdriver.Firefox(executable_path=exe_path)
        self.driver.implicitly_wait(3)

    def url_crawler(self):
        for i in range(1, 46):
            url_part_1 = 'https://kr.investing.com/stock-screener/?sp=country::11|'
            url_part_2 = 'sector::a|industry::a|equityType::a%3Ceq_market_cap;' + str(i)
            total_url = url_part_1 + url_part_2
            self.driver.get(total_url)

            xpath = "//table[@id='resultsTable']/tbody"
            element = self.driver.find_element_by_xpath(xpath)
            elements = [item.get_attribute('href') for item in element.find_elements_by_css_selector('a')]

            with open('total_url.txt', 'at') as f:
                for item in elements:
                    f.write(item + '\n')

    def auto_login(self, email, password):


        self.driver.get('https://kr.investing.com/')
        login = self.driver.find_element_by_link_text('로그인')
        login.click()

        login_id = self.driver.find_element_by_id('loginFormUser_email')
        login_id.send_keys(email)
        login_pw = self.driver.find_element_by_id('loginForm_password')
        login_pw.send_keys(password)

        login = self.driver.find_element_by_xpath("//div[@id='signup']/a")
        login.click()

    def download_csv(self, input_start_date, input_end_date):

        with open('seperated_1.txt', 'rt') as f:

            for key, URL in enumerate(f.readlines()):

                self.driver.get(URL)
                self.driver.implicitly_wait(3)

                self.driver.find_element_by_link_text('과거 데이터').click()
                self.driver.find_element_by_id('widgetFieldDateRange').click()

                start_date = self.driver.find_element_by_id('startDate')
                start_date.clear()
                start_date.send_keys(input_start_date)
                end_date = self.driver.find_element_by_id('endDate')
                end_date.clear()
                end_date.send_keys(input_end_date)
                self.driver.find_element_by_id('applyBtn').click()

                time.sleep(4)


                download = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='float_lang_base_2 downloadDataWrap']/a[@title='데이터 다운로드']")))
                download.click()

                stream = '( '+ str(key)+ ' / 100)' + 'done. '
                print(stream)




Stocks = SeleniumCrawler()
Stocks.auto_login(email='your_email', password='Your_password')
Stocks.download_csv(input_start_date='2012/01/01', input_end_date='2018/11/30')
