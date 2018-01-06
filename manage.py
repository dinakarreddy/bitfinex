import sys
from FinexAPI import FinexAPI
from websockets.main import main as websockets
from websockets.main import store_data
from websockets.candles import main as candles
from websockets.candles import take_position as take_position

def main():
    arguments = sys.argv[1:]
    if arguments[0] == 'websockets':
        # python manage.py websockets
        websockets()
    elif arguments[0] == 'store_data':
        # python manage.py store_data XRPUSD
        store_data(arguments[1])
    elif arguments[0] == 'candles':
        # python manage.py candles XRPUSD
        candles(arguments[1])
    elif arguments[0] == 'take_position':
        # python manage.py take_position XRPUSD
        take_position(arguments[1])
    else:
        print(FinexAPI.__dict__[arguments[0]](*arguments[1:]))


if __name__ == '__main__':
    main()
