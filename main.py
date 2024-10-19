from dotenv import load_dotenv
import requests
import hashlib
import os
import time
import hmac
import json


load_dotenv()
key: str = os.getenv("API_KEY")
secret: str = os.getenv("API_SECRET")

BASE_URL = "https://www.bitmex.com"
ORDER_URL = "/api/v1/order"
POSITION_URL = "/api/v1/position"
ACCOUNT_URL = "/api/v1/user/wallet"


def api_expires() -> str:
    return str(int(round(time.time()) + 30))


def api_signature(secret: str, verb: str, url: str, expiration: str, body: str):
    verb = verb
    path = url
    expiration = expiration
    if body != '':
        body = json.dumps(body)

    message = bytes(verb+path+expiration+body, "utf8")
    signature = hmac.new(bytes(secret, "utf8"), message, digestmod=hashlib.sha256).hexdigest()
    return signature


def get_balance():
    params = ""
    expire = api_expires()
    signature = api_signature(secret, "GET", ACCOUNT_URL + '?currency=USDt', expire, params)
    headers = {"api-expires": expire, "api-key": key, "api-signature": signature}
    response = requests.get(BASE_URL + ACCOUNT_URL + '?currency=USDt', headers=headers)
    wallet_bal = response.json()['amount']
    # print(f"wallet balance = {int(wallet_bal / 1000000)}")
    return int(wallet_bal / 1000000)


def create_order():
    entry_price = int(input("Enter entry price: "))
    params = {'symbol':'XBTUSDT','orderQty':1000,'ordType':'Limit','price':entry_price}
    expire = api_expires()
    signature = api_signature(secret, "POST", ORDER_URL, expire, params)
    headers = {"api-expires": expire, "api-key": key, "api-signature": signature}
    response = requests.post(BASE_URL + ORDER_URL, json=params, headers=headers)
    # print(response.json())



while True:
    direction = input("Enter Direction: ")

    if direction == "buy".lower() or direction == "sell".lower():
        entry_price = int(input("Enter entry price: "))
        stop_price = int(input("Enter stop price: "))
        risk_percent = float(input("Enter amount of risk: "))
        account_size = get_balance()

        if direction == "buy".lower():
            difference = (entry_price - stop_price) / entry_price
            break
        else:
            difference = (stop_price - entry_price) / entry_price
            break

    else:
        print("Input incorrect, try 'buy' or 'sell'")


risk_amount = account_size * risk_percent / 100
size = risk_amount / difference
print(f"Direction: {direction}, Entry: {entry_price}, Stop Loss: {stop_price}, Size: {round(size)}")