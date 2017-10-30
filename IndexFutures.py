"""

Author: Ian Doherty
Date: October 27, 2017



"""

# Imports
import quandl
import time
from pathlib import Path
from api_key import *

# Set API key
quandl.ApiConfig.api_key = api_key
quandl.ApiConfig.api_version = '2015-04-09'

# Count API calls. If api_calls >= 20: time.sleep(600)
api_calls = 0

#"CHRIS/CBOE_VIX3M",
# Instruments
instrument_list = [
    "CBOE/VXST",
    "CBOE/VIX",
    "CHRIS/CBOE_VX1",
    "CHRIS/CBOE_VX2",
    "CBOE/VXMT",
    "CBOE/VVIX",
]


class Instrument:
    """
    The instrument, represents one of the indexes or futures used in this script.
    """

    def __init__(self, symbol):

        self.symbol = symbol

        self.data = None

        pass

    def get_price_date(self):

        global api_calls

        print ('Getting prices', self.symbol)

        time_str = time.strftime('%Y%m%d')

        check_file = Path('./data/' + time_str + '-' + self.symbol.replace("/", "") + '.csv',)

        print (check_file.is_file())

        if check_file.is_file():
            pass
        else:
            self.data = quandl.get(self.symbol)
            write_to_file(self.data, self.symbol)
            api_calls = api_calls + 1

        pass

    pass


def write_to_file(data, name):
    """
    Writes data to files.

    """

    time_str = time.strftime('%Y%m%d')

    data.to_csv('./data/' + time_str + '-' + name.replace("/", "") + '.csv', index=True)

    pass


for index, value in enumerate(instrument_list):

    new_instrument = Instrument(value)
    new_instrument.get_price_date()

    instrument_list[index] = new_instrument

    print (instrument_list[index])

    pass


print (api_calls)
