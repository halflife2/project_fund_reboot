import ssl
import sys
import io
from os import chdir
import csv
import matplotlib as mpl
import matplotlib.pylab as plt

ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


class StockAccount:
    '''make csv to list from oldest data to latest data, and
       save as self.stock'''

    def __init__(self, file_name):

        #variable define


        # mean line variables define ( 5/ 10/ 30/ 60/ 120 days)
        self.stock_5_mean_line = []
        self.stock_30_mean_line = []
        self.stock_60_mean_line = []
        self.stock_120_mean_line = []
        self.stock_other_mean_line = []

        #change directory and save csv->self.stock
        chdir('/Users/ItsFriday/Documents/GitHub/project_fund/csv')

        with open(file_name, 'r', encoding='utf-8') as read_csv:
            lines = csv.reader(read_csv)
            self.stock = [line for line in list(lines)[-2:0:-1]]
            self.stock.insert(0, ['날짜', '현재가', '오픈', '고가', '저가', '거래량', '변동 %'])

        chdir('/Users/ItsFriday/Documents/GitHub/project_fund')

        self.slicing_price(self.stock)


    def mean_line(self, date):
        '''이동평균선
           5일 / 10일 / 30일 / 60일 / 120일 로 날짜 넣고 순서대로 작성'''
        stock_date_mean_line = []

        #slicing_stock = self.slicing_price()

        #pprint.pprint(slicing_stock)
        #make date woth zero
        for index in range(1, date+1):
            stock_date_mean_line.append([self.stock[index][0], 0])

        # 기준일 에서 date 만큼 이동평균선 만들기
        for index in range(date+1, len(self.stock)):
            mean = 0

            for row in range(index-date, index):
                mean += int(self.stock[row][1])
            mean = int(mean / date)

            stock_date_mean_line.append([self.stock[index][0], mean])


        # save each day_mean_line
        if date == 5:
            self.stock_5_mean_line = stock_date_mean_line
            return self.stock_5_mean_line
        elif date == 30:
            self.stock_30_mean_line = stock_date_mean_line
            return self.stock_30_mean_line
        elif date == 60:
            self.stock_60_mean_line = stock_date_mean_line
            return self.stock_60_mean_line
        elif date == 120:
            self.stock_120_mean_line = stock_date_mean_line
            return self.stock_120_mean_line
        else:
            self.stock_other_mean_line = stock_date_mean_line
            return self.stock_other_mean_line


    def slicing_price(self, stock):
        '''slice list '''

        # replace'M', 'k' and multiple x1000, x1000000

        for item in self.stock:

            if item[5][-1] == 'M':
                item[5] = item[5].replace('M', '')
                item[5] = int(float(item[5]) * 1000000)

            elif item[5][-1] == 'K':
                item[5].replace('K', '')
                item[5] = item[5].replace('K', '')
                item[5] = int(float(item[5]) * 1000)

            elif item[5] == '-':
                item[5] = 0

            # delete ',' with price
            item[1] = item[1].replace(',', '')
            item[2] = item[2].replace(',', '')
            item[3] = item[3].replace(',', '')
            item[4] = item[4].replace(',', '')

        return self.stock

    def plot_show(self):

        days = []
        prices = []

        for row in self.stock_30_mean_line:
            if row[1] > 0:
                days.append(row[0])
                prices.append(row[1])
            else:
                pass

        plt.title('mean line compare graph')
        plt.plot(days, prices, label='30 mean line')
        plt.ylabel('price')
        plt.xlabel('day')
        plt.show()



stock_000270 = StockAccount('000270 역사적 데이터.csv')
stock_000270.mean_line(30)
stock_000270.plot_show()
