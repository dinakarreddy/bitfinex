class LongPosition:
    def __init__(self, symbol, status='sold', file_name='{}_buy_sell_candle.txt'):
        self.status = status
        self.symbol = symbol
        self.prev_macd = None
        self.file_name = file_name.format(symbol)

    def update_position(self, macd, macd_signal, rsi, price, timestamp):
        args = [macd, macd_signal, rsi, price, timestamp]
        if len(list(filter(lambda x: x is None, args))) == 0:
            if self.status == 'bought':
                self.remove_position(macd, macd_signal, rsi, price, timestamp)
            elif self.status == 'sold':
                self.take_position(macd, macd_signal, rsi, price, timestamp)
        macd_diff = None
        if macd is not None and macd_signal is not None:
            macd_diff = macd - macd_signal
        temp = ','.join(map(lambda x: str(x), [self.status, macd_diff, macd, macd_signal, rsi, price, timestamp]))
        with open(self.file_name, 'a') as outfile:
                outfile.write(temp + '\n')
        self.prev_macd = macd

    def take_position(self, macd, macd_signal, rsi, price, timestamp):
        if (macd - macd_signal) > 0 and rsi < 30:
            self.status = 'bought'


    def remove_position(self, macd, macd_signal, rsi, price, timestamp):
        if (macd - macd_signal) < 0:
            self.status = 'sold'
        if rsi > 70 and macd < self.prev_macd:
            self.status = 'sold'
