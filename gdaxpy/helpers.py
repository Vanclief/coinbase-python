import calendar
import datetime

def dict_to_float(d):
    """
    Converts all strings to floats from a dict
    """
    if type(d) is dict:
        for key, value in d.items():
            if type(value) is str:
                try:
                    d[key] = float(value)
                except ValueError:
                    d[key] = str(value)

    return d


def list_dict_to_float(l):
    """
    Applies dict_to_float to all elements from a list
    """
    for d in l:
        d = dict_to_float(d)

    return l

def separate_symbols(s):
    """
    Adds a dash to a symbol pair. btcusd -> btc-usd
    """
    return s[:3] + '-' + s[3:]

def str_to_timestamp(s):

    d = datetime.datetime.strptime(s[:19], '%Y-%m-%dT%H:%M:%S')
    epoch = float(calendar.timegm(d.utctimetuple()))

    return epoch
