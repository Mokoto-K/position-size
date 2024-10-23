from dotenv import load_dotenv
import requests
import hashlib
import os
import time
import hmac
import json

# Environment variables for the api key and secret
load_dotenv()
APIKEY: str = os.getenv("API_KEY")
APISECRET: str = os.getenv("API_SECRET")

# Not the best system for urls but it will do for now
BASE_URL = "https://www.bitmex.com"
ORDER_URL = "/api/v1/order"
POSITION_URL = "/api/v1/position"
ACCOUNT_URL = "/api/v1/user/wallet"


def api_signature(verb: str, url: str, body: dict or str):
    """Gets the auth signature for bitmex and returns it as well as the rest of the header needed to auth a query
        to the exchange.
    """

    # HTML Method for querying api
    verb = verb

    # The url to query, have to slice the base url out for now until I find a better way to match auth with request
    path = url[22:]

    # Expire time needed by exchange to prevent relay attacks
    expire = str(int(round(time.time()) + 30))

    # Only include the body to the signature if it exists, else dw about it
    if body != '':
        body = json.dumps(body)

    # Concatenate the message and convert it to bytes, get the signature and return it with the rest of the header
    message = bytes(verb + path + expire + body, "utf8")
    signature = hmac.new(bytes(APISECRET, "utf8"), message, digestmod=hashlib.sha256).hexdigest()
    return {"api-expires": expire, "api-key": APIKEY, "api-signature": signature}


def get_balance(params=None):
    """
    Gets the wallet balance of a currency for user, default is btc is none is specified

    Can specify which currency you want to get by sending in a dict e.g {"currency":"USDt"} for usdt
    """
    # Deals with the case of the user not specifying a currency to query
    if params is None:
        params = {}
    params = params

    # Creates the url for the auth request, gets the headers and returns the amount in the wallet
    url = requests.get(BASE_URL + ACCOUNT_URL, params=params).url
    headers = api_signature("GET", url, '')
    response = requests.get(url, headers=headers)

    return round(int(response.json()['amount']) / 1000000)


def create_order(symbol: str, side: str, ordtype: str, price: int, orderqty: int):
    """Makes an order from your desired parameters

    :param symbol: Symbol of the currency e.g. XBTUSDT
    :param side: "Buy" or "Sell"
    :param ordtype: 'Limit' or 'Market'
    :param orderqty: Size of your order
    :param price: Price to set order at
    :return:
    None
    """

    json_params = {'symbol': symbol, 'buy':side, 'ordType': ordtype, 'price': price, 'orderQty': orderqty}

    headers = api_signature("POST", BASE_URL + ORDER_URL, json_params)
    requests.post(BASE_URL + ORDER_URL, json=json_params, headers=headers)

    # TODO - Print better logging info
    print(f"{symbol} {side} {ordtype} order placed at {price} for {orderqty} contracts.")