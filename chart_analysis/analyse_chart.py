import ssl
import sys
import io
from os import chdir
import csv
import matplotlib as mpl
import matplotlib.pylab as plt
import pprint

ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


class StockAccount:
    '''make csv to list from oldest data to latest data, and
       save as self.stock'''

    def __init__(self, file_name):

        #self.variable define


        # mean line self.variables define ( 5/ 30/ 60/ 120 days)
        self.stock_5_mean_line = []
        self.stock_30_mean_line = []
        self.stock_60_mean_line = []
        self.stock_120_mean_line = []

        #change directory and save csv->self.stock
        chdir('/Users/ItsFriday/Documents/GitHub/project_fund/csv')

        with open(file_name, 'r', encoding='utf-8') as read_csv:
            lines = csv.reader(read_csv)
            self.stock = [line for line in list(lines)[-2:0:-1]]
            self.stock.insert(0, ['날짜', '현재가', '오픈', '고가', '저가', '거래량', '변동 %'])

        chdir('/Users/ItsFriday/Documents/GitHub/project_fund')

        self.list_slice(self.stock)


    def mean_line(self, date):
        '''이동평균선
           5일 / 30일 / 60일 / 120일 로 날짜 넣고 순서대로 작성'''
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


    def list_slice(self, stock):
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

            #frame date
            item[0] = item[0].replace('년', '-').replace(' ', '')
            item[0] = item[0].replace('월', '-').replace('일', '')

            # delete ',' with price
            item[1] = item[1].replace(',', '')
            item[2] = item[2].replace(',', '')
            item[3] = item[3].replace(',', '')
            item[4] = item[4].replace(',', '')

        return self.stock

    def plot_show(self, stock1, stock2):


        label_1, mean_1 = self.make_mean_label(stock1)
        label_2, mean_2 = self.make_mean_label(stock2)

        min_mean = min(mean_1, mean_2)

        minimal_days = [row[0] for row in self.stock[min_mean+1::400]]
        minimal_days.append(self.stock[-1][0])

        days_1, prices_1 = make_values(stock1)
        days_2, prices_2 = make_values(stock2)

        plt.title('mean line compare graph')


        plt.plot(days_1, prices_1, 'r', label=label_1)
        plt.plot(days_2, prices_2, 'b', label=label_2)
        plt.xticks(minimal_days)


        plt.legend(loc='upper right')

        plt.ylabel('price')
        plt.xlabel('days')
        plt.show()

    def make_mean_label(self, stock):

        if stock == self.stock_5_mean_line:
            label = '5 mean line'
            mean = 5
        elif stock == self.stock_30_mean_line:
            label = '30 mean line'
            mean = 30
        elif stock == self.stock_60_mean_line:
            label = '60 mean line'
            mean = 60
        elif stock == self.stock_120_mean_line:
            label = '120 mean line'
            mean = 120

        return label, mean

def make_values(mean_lined_list):

    days = [row[0] for row in mean_lined_list if row[1] > 0]
    prices = [row[1] for row in mean_lined_list if row[1] > 0]

    return days, prices


#make buttons
Stock_ = StockAccount('005940 역사적 데이터.csv')

mean_5 = Stock_.mean_line(5)
mean_30 = Stock_.mean_line(30)
mean_60 = Stock_.mean_line(60)
mean_120 = Stock_.mean_line(120)

Stock_.plot_show(mean_5, mean_120)
