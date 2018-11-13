from yahoo_finance import Share

samsung = Share('005930.KS')
print(samsung.get_open())
print(samsung.get_price())