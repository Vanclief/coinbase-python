from gdaxpy.requester import Requester
import gdaxpy.helpers as helpers

TICKER_URL = "/ticker"
ORDERS_URL = "/book?level=2"
TRADES_URL = "trades/"
PRODUCTS_URL = "products/"


class Market(object):

    def __init__(self, api_base):
        self.r = Requester(api_base)

    def get_ticker(self, symbol):

        product = helpers.separate_symbols(symbol)
        endpoint = (PRODUCTS_URL + product + TICKER_URL)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        ticker = {}
        ticker['ask'] = float(response['ask'])
        ticker['bid'] = float(response['bid'])
        ticker['mid'] = ((ticker['ask'] + ticker['bid']) / 2)
        ticker['last_price'] = float(response['price'])
        ticker['low'] = float(0)
        ticker['high'] = float(0)
        ticker['volume'] = float(response['volume'])
        ticker['timestamp'] = helpers.str_to_timestamp(response['time'])

        return status, ticker

    def get_orderbook(self, symbol):

        product = helpers.separate_symbols(symbol)
        endpoint = (PRODUCTS_URL + product + ORDERS_URL)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        order_book = {'asks': [], 'bids': []}

        for order_type in response.keys():
            for value in response[order_type]:
                # for value in values

                print(value)
                print(value[0])
                print(value[1])
                order = {}
                order['price'] = float(value[0])
                # order['amount'] = float(value[1])
                # order['timestamp'] = float(value[2])

                if order_type == 'asks':
                    order_book['asks'].append(order)
                elif order_type == 'bids':
                    order_book['bids'].append(order)

        return status, order_book

    def get_trades(self, symbol):
        endpoint = TRADES_URL + symbol
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        return status, helpers.list_dict_to_float(response)

    def get_symbols(self):
        endpoint = SYMBOLS_URL
        return self.r.get(endpoint)

    def get_symbol_details(self):
        endpoint = SYMBOL_DETAILS
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        return status, helpers.list_dict_to_float(response)
