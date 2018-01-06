import csv

def csv_reader(file, delimiter=','):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row



def main():
    # header = 'status,macd_diff,macd,signal,rsi,price,timestamp'
    # file = 'test_buy_sell_candle_btc_sample.txt'
    file = 'new_XRPUSD_buy_sell_candle.txt'
    status = 'sold'
    profit = 0
    profit_percent = 0
    bought_price = None
    num_of_transactions = 0
    num_gain_transactions = 0
    num_loss_transactions = 0
    for row in csv_reader(file):
        if row['status'] != status:
            row['price'] = float(row['price'])
            if row['status'] == 'bought':
                bought_price = row['price']
            if row['status'] == 'sold':
                curr_profit = row['price'] - bought_price
                curr_profit_percent = 100*float(curr_profit)/bought_price
                print(profit, profit_percent, curr_profit, curr_profit_percent, num_of_transactions, num_loss_transactions, num_gain_transactions)
                if curr_profit > 0:
                    num_gain_transactions += 1
                else:
                    num_loss_transactions += 1
                profit += curr_profit
                profit_percent += curr_profit_percent
                bought_price = None
                num_of_transactions += 1
            status = row['status']
    print(profit, profit_percent, num_of_transactions, num_loss_transactions, num_gain_transactions)

if __name__ == '__main__':
    main()
