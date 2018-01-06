import datetime
from collections import deque
from .config import MULTIPLIER

class MACD:
    def __init__(self, fast_len=12, slow_len=26, signal_len=9):
        self.source = 'open' # can be open, high, low or close
        self.moving_avgs = {
            'fast': {
                'values': deque(),
                'ema_value': None,
                'multiplier': MULTIPLIER(fast_len),
                'len': fast_len,
            },
            'slow': {
                'values': deque(),
                'ema_value': None,
                'multiplier': MULTIPLIER(slow_len),
                'len': slow_len,
            }
        }
        self.macd = {
            'macd_values': deque(),
            'len': signal_len,
            'multiplier': MULTIPLIER(signal_len),
            'signal': None,
            'macd': None,
        }


    def update(self, price):
        if not price:
            return
        # update emas
        for key in self.moving_avgs:
            self.moving_avgs[key]['values'].appendleft(price)
            if len(self.moving_avgs[key]['values']) == self.moving_avgs[key]['len']:
                if self.moving_avgs[key]['ema_value'] is None:
                    self.moving_avgs[key]['ema_value'] = float(sum(self.moving_avgs[key]['values']))/self.moving_avgs[key]['len']
                else:
                    self.moving_avgs[key]['ema_value'] = ((price - self.moving_avgs[key]['ema_value']) * self.moving_avgs[key]['multiplier']) + self.moving_avgs[key]['ema_value']
                self.moving_avgs[key]['values'].pop()

        #update macds
        if self.moving_avgs['fast']['ema_value'] and self.moving_avgs['slow']['ema_value']:
            macd = self.moving_avgs['fast']['ema_value'] - self.moving_avgs['slow']['ema_value']
            self.macd['macd_values'].appendleft(macd)
            self.macd['macd'] = macd
            if len(self.macd['macd_values']) == self.macd['len']:
                if self.macd['signal'] is None:
                    self.macd['signal'] = float(sum(self.macd['macd_values']))/self.macd['len']
                else:
                    self.macd['signal'] = ((self.macd['macd'] - self.macd['signal']) * self.macd['multiplier']) + self.macd['signal']
                self.macd['macd_values'].pop()
