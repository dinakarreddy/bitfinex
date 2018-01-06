from btfxwss import BtfxWss
import time
import sys
import csv
from .candle_indicators import macd, rsi
from .positions import LongPosition
import datetime
import json
import os

CANDLE_FILE_LOCATION = "/Users/caesar/Desktop/bitfinex/bitfinex/websockets/candle_files/{symbol}/"


def get_candle_q(symbol):
    """
        candle_format: ([[1515066900000, 3.1354, 3.1457, 3.1459, 3.1261, 41373.42748331]], 1515066939.756591)
                        ([[candle_time, O, H, L, C]], timestamp)
    """
    wss = BtfxWss()
    wss.start()

    while not wss.conn.connected.is_set():
        time.sleep(1)

    valid_candles = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D',
                     '7D', '14D', '1M']
    wss.subscribe_to_candles(symbol, '1m')

    time.sleep(15)
    candles_q = wss.candles(symbol, '1m')
    return candles_q

def main(symbol):
    file_dir = CANDLE_FILE_LOCATION.format(symbol=symbol)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    candles_q = get_candle_q(symbol)
    while 1:
        if candles_q.empty():
            time.sleep(1)
        else:
            candle = candles_q.get()
            print(symbol, 'candle', candle)
            with open(file_dir + datetime.datetime.now().strftime("%Y%m%d") + '.txt', 'a') as outfile:
                outfile.write(str(candle))
                outfile.write('\n')



def get_price_timestamp(symbol):
    candles_q = get_candle_q(symbol)
    while 1:
        if candles_q.empty():
            time.sleep(1)
        else:
            candle = candles_q.get()
            timestamp = candle[0][0][0]
            price = candle[0][0][1]
            if not isinstance(price, list):
                yield (price, timestamp)


def csv_reader(file, delimiter=','):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row

def get_price_from_csv():
    filename = '/Users/caesar/Downloads/coinbaseUSD_1-min_data_2014-12-01_to_2017-10-20.csv.csv'
    for row in csv_reader(filename):
        yield (float(row['Open']), float(row['Timestamp']))



def take_position(symbol):
    macd_obj = macd.MACD()
    rsi_obj = rsi.RSI()
    long_position = LongPosition(symbol)
    last_timestamp = None
    for (price, timestamp) in get_price_timestamp(symbol):
    # for (price, timestamp) in get_price_from_csv():
        print(price, timestamp)
        if last_timestamp:
            if timestamp <= last_timestamp:
                continue
            if (timestamp - last_timestamp > 60000):
            # if (timestamp - last_timestamp > 60):
                print("************\n\n\n*********\n\n\n Resetting \n**********\n\n\n*********\n\n\n")
                macd_obj = macd.MACD()
                rsi_obj = rsi.RSI()
                long_position.status = 'sold'
                # should remove position if present as continous data lost
        last_timestamp = timestamp
        macd_obj.update(price)
        rsi_obj.update(price)
        long_position.update_position(macd_obj.macd['macd'], macd_obj.macd['signal'], rsi_obj.rsi['rsi'], price, timestamp)
        # print(macd_obj.moving_avgs)
        # print(macd_obj.macd)


if __name__ == '__main__':
    main('XRPUSD')
