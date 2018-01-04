from gdaxpy.requester import Requester
import gdaxpy.helpers as helpers

TIME_URL = "time"
TICKER_URL = "/ticker"
ORDERS_URL = "/book?level=2"
TRADES_URL = "/trades"
PRODUCTS_URL = "products/"


class Market(object):

    def __init__(self, api_base):
        self.r = Requester(api_base)

    def get_server_time(self):
        endpoint = TIME_URL
        status, reponse = self.r.get(endpoint)

        if status != 200:
            return status, response['message']

        return status, reponse

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

        # We need to first manually get the timestamp, since
        # Gdax doesn't include it ...
        status, response = self.get_server_time()

        if status != 200:
            return status, response

        timestamp = response['epoch']


        product = helpers.separate_symbols(symbol)
        endpoint = (PRODUCTS_URL + product + ORDERS_URL)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        order_book = {'asks': [], 'bids': []}

        for order_type, orders in response.items():
            for value in orders:
                if order_type in ['bids', 'asks']:
                    order = {}
                    order['price'] = float(value[0])
                    order['amount'] = float(value[1])
                    order['timestamp'] = timestamp

                    if order_type == 'asks':
                        order_book['asks'].append(order)
                    elif order_type == 'bids':
                        order_book['bids'].append(order)

        return status, order_book

    def get_trades(self, symbol):

        product = helpers.separate_symbols(symbol)
        endpoint = (PRODUCTS_URL + product + TRADES_URL)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        trades = []

        for value in response:

            trade = {}
            trade['timestamp'] = helpers.str_to_timestamp(
                    value['time'])
            trade['tid'] = int(value['trade_id'])
            trade['price'] = float(value['price'])
            trade['amount'] = float(value['size'])
            trade['exchange'] = 'Gdax'
            trade['type'] = value['side']

            trades.append(trade)

        return status, trades

    def get_symbols(self):
        endpoint = PRODUCTS_URL
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        symbols = []

        for product in response:
            symbol = helpers.join_symbols(product['id'])
            symbols.append(symbol)

        return status, symbols

    def get_symbol_details(self):
        endpoint = PRODUCTS_URL
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        symbols = []

        for product in response:
            symbol = {}
            symbol['pair'] = helpers.join_symbols(product['id'])
            symbol['price_precision'] = 5
            symbol['initial_margin'] = 0.0
            symbol['minimum_margin'] = 0.0
            symbol['minimum_order_size'] = float(
                    product['base_min_size'])
            symbol['maximum_order_size'] = float(
                    product['base_max_size'])
            symbol['expiration'] = 'NA'
            symbols.append(symbol)


        return status, symbols
