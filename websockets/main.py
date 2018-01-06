from btfxwss import BtfxWss
import time
import sys
from .indicators import macd, rsi
from .positions import LongPosition
import datetime
import json
import os

TICKER_FILE_LOCATION = "/Users/caesar/Desktop/bitfinex/bitfinex/websockets/ticker_files/{symbol}/"
TRADE_FILE_LOCATION = "/Users/caesar/Desktop/bitfinex/bitfinex/websockets/trade_files/{symbol}/"


def parse_ticker(ticker):
    # ticker = ([[2.1524, 102891.82706453, 2.1578, 169533.05006635, 0.341, 0.1884, 2.151, 85626133.66420326, 2.196, 1.8201]], 1514903073.135506)
    return ','.join(list(map(lambda x: str(x), ticker[0][-1])) + [str(ticker[1])]) + '\n'

def main():
    wss = BtfxWss()
    wss.start()
    macd_obj = macd.MACD()
    rsi_obj = rsi.RSI()
    long_position = LongPosition()

    while not wss.conn.connected.is_set():
        time.sleep(1)

    # wss.subscribe_to_ticker('XRPUSD')
    wss.subscribe_to_trades('XRPUSD')

    time.sleep(15)
    
    # ticker_q = wss.tickers('XRPUSD')  # returns a Queue object for the pair.
    ticker_q = wss.trades('XRPUSD')
    while 1:
        if ticker_q.empty():
            time.sleep(1)
        else:
            ticker = ticker_q.get()
            print(ticker)
            # price = ticker[0][-1][6]
            # timestamp = ticker[1]
            timestamp = ticker[1]
            price = ticker[0][-1][-1]
            if isinstance(price, list):
                continue
            macd_obj.update_macd(timestamp, price)
            # print(macd_obj.macds)
            rsi_obj.update_rsi(timestamp, price)
            # print(rsi_obj.rsi)
            long_position.update_position(macd_obj.macds['present_macd'], macd_obj.macds['present_signal'], rsi_obj.rsi['rsi'], price, timestamp)
            # print('\n\n')


def store_data(symbol):
    file_dir = TRADE_FILE_LOCATION.format(symbol=symbol)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    wss = BtfxWss()
    wss.start()
    while not wss.conn.connected.is_set():
        time.sleep(1)
    wss.subscribe_to_trades(symbol)
    time.sleep(15)
    trade_q = wss.trades(symbol)
    while 1:
        if trade_q.empty():
            time.sleep(1)
        else:
            trade = trade_q.get()
            with open(file_dir + datetime.datetime.now().strftime("%Y%m%d") + '.txt', 'a') as outfile:
                outfile.write(str(trade))
                outfile.write('\n')
            print(trade)


if __name__ == '__main__':
    main()
