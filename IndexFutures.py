"""

Author: Ian Doherty
Date: October 27, 2017



"""

# Imports
import quandl
import time
from pathlib import Path
from api_key import *
import os

# Set API key
quandl.ApiConfig.api_key = api_key
quandl.ApiConfig.api_version = '2015-04-09'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

os.environ['TZ'] = 'US/Eastern'
time.tzset()
print (time.tzname)

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

        time_str = time.strftime('%Y%m%d', time.localtime())

        print ('Checking: ', time_str)

        check_file = Path(ROOT_DIR + '/data/' + time_str + '-' + self.symbol.replace("/", "") + '.csv',)

        if check_file.is_file():
            print ('File already existed.')
            pass
        else:
            print ('File did not exist and will be created.')
            self.data = quandl.get(self.symbol)
            write_to_file(self.data, self.symbol)

        pass

    pass


def write_to_file(data, name):
    """
    Writes data to files.

    """

    time_str = time.strftime('%Y%m%d', time.localtime())

    data.to_csv(Path(ROOT_DIR + '/data/' + time_str + '-' + name.replace("/", "") + '.csv'), index=True)

    pass


for index, value in enumerate(instrument_list):

    new_instrument = Instrument(value)
    new_instrument.get_price_date()

    instrument_list[index] = new_instrument

    pass

