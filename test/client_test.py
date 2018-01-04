from gdaxpy.gdax import Gdax
import httpretty

client = Gdax()

def set_time_endpoint():

    mock_body = (
            '{"iso": "2015-01-07T23:47:25.201Z",' +
            '"epoch": 1420674445.201}'
            )

    mock_url = client.api_base + '/time'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )


def test_should_have_correct_url():
    g = Gdax()
    assert g.api_base == 'https://api.gdax.com/'


def test_should_have_api_key():
    g = Gdax('974554aed089', '2976be9e189d')
    assert g.api_key == '974554aed089'


def test_should_have_secret_key():
    g = Gdax('974554aed089', '2976be9e189d')
    assert g.api_secret == '2976be9e189d'

@httpretty.activate
def test_should_return_ticker():

    mock_symbol = 'btcusd'
    mock_body = (
            '{"trade_id": 4729088,"price": "333.99","size": "0.193",' +
            '"bid": "333.98","ask": "333.99",' +
            '"volume": "5957.11914015",' +
            '"time": "2015-11-14T20:46:03.511254Z"}'
            )
    mock_url = client.api_base + 'products/btc-usd/ticker'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = {
            "mid": 333.985,
            "bid": 333.98,
            "ask": 333.99,
            "last_price": 333.99,
            "low": 0.0,
            "high": 0.0,
            "volume": 5957.11914015,
            "timestamp": 1447533963.0
            }

    response = client.ticker(mock_symbol)
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_orderbook():

    set_time_endpoint()

    mock_symbol = 'btcusd'
    mock_body = (
            '{"sequence": "3","bids": [["295.96","4.39088265", 2 ]], ' +
            '"asks":[["295.97", "25.23542881", 12 ]]}'
            )
    mock_url = client.api_base + 'products/btc-usd/book?level=2'

    print(mock_url, 'Mock')
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = {
            "bids": [
                {
                    "price": 295.96,
                    "amount": 4.39088265,
                    "timestamp": 1.0
                    }
                ],
            "asks": [
                {
                    "price": 295.97,
                    "amount": 25.23542881,
                    "timestamp": 1.0
                    }
                ]
            }

    response = client.orderbook(mock_symbol)
    assert expected_response == response[1]


"""
@httpretty.activate
def test_should_return_trades():

    mock_symbol = 'btcusd'
    mock_body = (
            '[{"time": "2014-11-07T22:19:28.578544Z", "trade_id": 74,' +
            '"price": "10.00000000","size": "0.01000000","side": "buy"' +
            '}]'
            )
    mock_url = client.api_base + 'btc-usd' + '/trades'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = [
            {"timestamp": 1444266681, "tid": 74, "price": 10.0,
                "amount": 0.01, "exchange": "Gdax", "type": "buy"}
            ]

    response = client.trades(mock_symbol)
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_symbols():


    mock_body = (
            '[{"id":"BCH-USD","base_currency":"BCH","quote_currency":"USD",' +
            '"base_min_size":"0.0001","base_max_size":"250",' +
            '"quote_increment":"0.01","display_name":"BCH/USD",' +
            '"status":"online","margin_enabled":false,"status_message":null},' +
            '{"id":"LTC-EUR","base_currency":"LTC","quote_currency":"EUR",' +
            '"base_min_size":"0.01","base_max_size":"1000000",' +
            '"quote_increment":"0.01","display_name":"LTC/EUR"' +
            ',"status":"online","margin_enabled":false' +
            ',"status_message":null},{"id":"LTC-USD","base_currency":"LTC"' +
            ',"quote_currency":"USD","base_min_size":"0.01"' +
            ',"base_max_size":"1000000","quote_increment":"0.01"' +
            ',"display_name":"LTC/USD","status":"online"' +
            ',"margin_enabled":false,"status_message":null}]'
            )

    mock_url = client.api_base + '/products'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = ["bchusd", "ltceur", "ltcusd"]

    response = client.symbols()
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_symbol_details():

    mock_body = (
            '[{"id":"BCH-USD","base_currency":"BCH","quote_currency":"USD",' +
            '"base_min_size":"0.0001","base_max_size":"250",' +
            '"quote_increment":"0.01","display_name":"BCH/USD",' +
            '"status":"online","margin_enabled":false,"status_message":null},' +
            '{"id":"LTC-EUR","base_currency":"LTC","quote_currency":"EUR",' +
            '"base_min_size":"0.01","base_max_size":"1000000",' +
            '"quote_increment":"0.01","display_name":"LTC/EUR"' +
            ',"status":"online","margin_enabled":false' +
            ',"status_message":null},{"id":"LTC-USD","base_currency":"LTC"' +
            ',"quote_currency":"USD","base_min_size":"0.01"' +
            ',"base_max_size":"1000000","quote_increment":"0.01"' +
            ',"display_name":"LTC/USD","status":"online"' +
            ',"margin_enabled":false,"status_message":null}]'
            )
    mock_url = client.api_base + '/products'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = [
            {
                "pair": "bchusd", "price_precision": 5,
                "initial_margin": 0.0, "minimum_margin": 0.0,
                "maximum_order_size": 250.0, "minimum_order_size": 0.0001,
                "expiration": "NA"
                },
            {
                "pair": "ltceur", "price_precision": 5,
                "initial_margin": 0.0, "minimum_margin": 0.0,
                "maximum_order_size": 1000000.0, "minimum_order_size": 0.01,
                "expiration": "NA"
                },
            {
                "pair": "ltcusd", "price_precision": 5,
                "initial_margin": 0.0, "minimum_margin": 0.0,
                "maximum_order_size": 1000000.0, "minimum_order_size": 0.01,
                "expiration": "NA"
                }
            ]
    response = client.symbol_details()
    assert expected_response == response[1]
"""
