CANDLES = {
    'minute': {'second': 0},
    'hour': {'second': 0, 'minute': 0},
    'day': {'second': 0, 'minute': 0, 'hour': 0},
}

TIME_DIFF = {
    'minute': 60,
    'hour': 60*60,
    'day': 60*60*24,
}

MULTIPLIER = lambda period: 2.0/(period + 1)
