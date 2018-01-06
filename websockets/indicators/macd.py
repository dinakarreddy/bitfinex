import datetime
from collections import deque
from .config import CANDLES, TIME_DIFF, MULTIPLIER

class MACD:
    def __init__(self, fast_len=12, slow_len=26, signal_len=9, candle_duration='minute'):
        self.source = 'close' # can be open, high, low or close
        self.round_off = CANDLES[candle_duration]
        self.time_diff = TIME_DIFF[candle_duration]
        self.last_time = None
        self.last_price = None
        self.macds = {
            'values': deque(),
            'len': signal_len,
            'signal': deque(),
            'multiplier': MULTIPLIER(signal_len),
            'present_signal': None,
            'present_macd': None,
        }
        self.moving_avgs = {
            'fast': {
                'values': deque(),
                'ema_values': deque(),
                'multiplier': MULTIPLIER(fast_len),
                'len': fast_len,
                'present_ema': None,
            },
            'slow': {
                'values': deque(),
                'ema_values': deque(),
                'multiplier': MULTIPLIER(slow_len),
                'len': slow_len,
                'present_ema': None
            }
        }

    def reset(self, present_time, present_price):
        """
            called when there is break in data
        """
        self.last_time = present_time
        self.last_price = present_price
        self.macds.update({
            'values': deque(),
            'signal': deque(),
            'present_signal': None,
            'present_macd': None,
        })
        for key in self.moving_avgs:
            self.moving_avgs[key].update({
                'values': deque(),
                'ema_values': deque(),
                'present_ema': None,
            })

    def update_macd(self, timestamp, present_price):
        # trade = (['tu', [150146740, 1514905858297, -115.6019607, 2.1274]], 1514905858.8471382)
        # ticker = ([[2.1524, 102891.82706453, 2.1578, 169533.05006635, 0.341, 0.1884, 2.151, 85626133.66420326, 2.196, 1.8201]], 1514903073.135506)
        present_time = datetime.datetime.fromtimestamp(int(timestamp)).replace(**self.round_off)
        if not(present_time == self.last_time or self.last_time is None):
            if int((present_time - self.last_time).total_seconds() - self.time_diff) != 0:
                print("Reset at times: {present_time}, {last_time}".format(
                    present_time=present_time,
                    last_time=self.last_time))
                self.reset(present_time, present_price)
                return
            for key in self.moving_avgs:
                self.moving_avgs[key]['values'].appendleft(self.last_price)
                self.calculate_ema(self.moving_avgs[key], self.last_price)
            self.calculate_macd()
        self.last_price = present_price
        self.last_time = present_time

    @staticmethod
    def calculate_ema(_dict, present_price):
        """
            Initial SMA: 10-period sum / 10 
            Multiplier: (2 / (Time periods + 1) ) = (2 / (10 + 1) ) = 0.1818 (18.18%)
            EMA: {Close - EMA(previous day)} x multiplier + EMA(previous day).

            At the start SMA = EMA(previousday)
        """
        ema = None
        if len(_dict['values']) == _dict['len']:
            try:
                prev_ema = _dict['ema_values'].pop()
            except IndexError:
                prev_ema = None

            if prev_ema is None:
                # happens for the first time `len` elements in values
                ema = float(sum(_dict['values']))/_dict['len']
            else:
                ema = ((present_price - prev_ema) * _dict['multiplier']) + prev_ema
            _dict['values'].pop()
        _dict['ema_values'].appendleft(ema)
        _dict['present_ema'] = ema


    def calculate_macd(self):
        if self.moving_avgs['fast']['present_ema'] and self.moving_avgs['slow']['present_ema']:
            macd = self.moving_avgs['fast']['present_ema'] - self.moving_avgs['slow']['present_ema']
            self.calculate_macd_signal(macd)
        else:
            macd = None

    def calculate_macd_signal(self, macd):
        self.macds['values'].appendleft(macd)
        signal = None
        if len(self.macds['values']) == self.macds['len']:
            try:
                prev_signal = self.macds['signal'].pop()
            except IndexError:
                prev_signal = None

            if prev_signal is None:
                signal = float(sum(self.macds['values']))/self.macds['len']
            else:
                signal = ((macd - prev_signal) * self.macds['multiplier']) + prev_signal
            self.macds['values'].pop()
        self.macds['signal'].appendleft(signal)
        self.macds['present_signal'] = signal
        self.macds['present_macd'] = macd




