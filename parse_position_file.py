from websockets.positions import LongPosition
import sys
import csv


def csv_reader(file, delimiter=','):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row


def get_value(value):
    if value == 'None':
        return None
    else:
        return float(value)

def main(symbol):
    file = '{}_buy_sell_candle.txt'.format(symbol)
    status = 'sold'
    profit = 0
    profit_percent = 0
    bought_price = None
    num_of_transactions = 0
    num_gain_transactions = 0
    num_loss_transactions = 0
    long_position_obj = LongPosition(symbol, file_name='new_{}_buy_sell_candle.txt')
    for row in csv_reader(file):
        long_position_obj.update_position(
            get_value(row['macd']),
            get_value(row['signal']),
            get_value(row['rsi']),
            get_value(row['price']),
            get_value(row['timestamp']))

if __name__ == '__main__':
    main(sys.argv[1])
