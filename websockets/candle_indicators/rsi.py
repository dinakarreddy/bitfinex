import datetime
from collections import deque
from .config import MULTIPLIER


class RSI:
    def __init__(self, duration=14, candle_duration='minute'):
        self.source = 'open' # can be open, high, low or close
        self.rsi = {
            'prev_price': None,
            'gain': deque(),
            'loss': deque(),
            'len': duration,
            'rsi': None
        }

    def update(self, price):
        if self.rsi['prev_price'] is not None:
            # calculate loss and gain w.r.t rsi['price']
            gain = 0
            loss = 0
            if self.rsi['prev_price'] < price:
                gain = price - self.rsi['prev_price']
            else:
                loss = self.rsi['prev_price'] - price
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
        self.rsi['prev_price'] = price
