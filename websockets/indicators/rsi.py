import datetime
from collections import deque
from .config import CANDLES, TIME_DIFF, MULTIPLIER


class RSI:
    def __init__(self, duration=14, candle_duration='minute'):
        self.source = 'close' # can be open, high, low or close
        self.round_off = CANDLES[candle_duration]
        self.time_diff = TIME_DIFF[candle_duration]
        self.last_time = None
        self.last_price = None
        self.rsi = {
            'price': None,
            'gain': deque(),
            'loss': deque(),
            'len': duration,
            'rsi': None
        }

    def reset(self, present_time, present_price):
        """
            called when there is break in data, due to network issues
        """
        self.last_time = present_time
        self.last_price = present_price
        self.rsi.update({
            'price': None,
            'gain': deque(),
            'loss': deque(),
            'rsi': None,
        })


    def update_rsi(self, timestamp, present_price):
        present_time = datetime.datetime.fromtimestamp(int(timestamp)).replace(**self.round_off)
        if not(present_time == self.last_time or self.last_time is None):
            if int((present_time - self.last_time).total_seconds() - self.time_diff) != 0:
                print("Reset at times: {present_time}, {last_time}".format(
                    present_time=present_time,
                    last_time=self.last_time))
                self.reset(present_time, present_price)
                return
            if self.rsi['price'] is not None:
                # calculate loss and gain w.r.t rsi['price']
                gain = 0
                loss = 0
                if self.rsi['price'] < self.last_price:
                    gain = self.last_price - self.rsi['price']
                else:
                    loss = self.rsi['price'] - self.last_price
                self.rsi['gain'].appendleft(gain)
                self.rsi['loss'].appendleft(loss)
                if len(self.rsi['gain']) == self.rsi['len']:
                    loss_sum = sum(self.rsi['loss'])
                    gain_sum = sum(self.rsi['gain'])
                    if loss_sum == 0:
                        self.rsi['rsi'] = 100.0
                    else:
                        self.rsi['rsi'] = 100.0 - (100.0/(1+(float(gain_sum)/loss_sum)))
                    self.rsi['gain'].pop()
                    self.rsi['loss'].pop()
            self.rsi['price'] = self.last_price
        self.last_price = present_price
        self.last_time = present_time
