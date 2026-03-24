import http.client
import json
import ssl
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")


def get_figi(ticker):
    ssl_context = make_ssl()
    
    conn = http.client.HTTPSConnection(
        "invest-public-api.tbank.ru", 
        context=ssl_context
    )

    payload = json.dumps({
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    conn.request("POST", "/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/GetAssets", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    for i in json_data["assets"]:
        if ticker == i["instruments"][0]["ticker"]:
            # return i["instruments"][0]["figi"]
            return i["instruments"][0]["figi"]
    
    return None


def get_candles(figi, date_from, date_to, interval):
    ssl_context = make_ssl()

    conn = http.client.HTTPSConnection(
        "invest-public-api.tbank.ru", 
        context=ssl_context
    )

    payload = json.dumps({
        "from": f"{date_from}",
        "to": f"{date_to}",
        "interval": f"{interval}",
        "instrumentId": f"{figi}",
        "candleSourceType": "CANDLE_SOURCE_UNSPECIFIED"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    conn.request("POST", "/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(json.loads(data))
    for i in json.loads(data)["candles"]:
        print(i, "\n")
    return json.loads(data)["candles"]


def get_bond_figi(name):
    ssl_context = make_ssl()

    conn = http.client.HTTPSConnection(
        "invest-public-api.tbank.ru", 
        context=ssl_context
    )

    payload = json.dumps({
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    conn.request("POST", "/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/Bonds", payload, headers)
    res = conn.getresponse()
    data = res.read()
    res_data = json.loads(data)["instruments"]

    for i in res_data:
        if name == i["ticker"]:
            return i["figi"]
    return None


def get_currency_figi_by_name(ticker):
    ssl_context = make_ssl()

    conn = http.client.HTTPSConnection(
        "invest-public-api.tbank.ru", 
        context=ssl_context
    )

    payload = json.dumps({
        "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED",
        "instrumentExchange": "INSTRUMENT_EXCHANGE_UNSPECIFIED"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    conn.request("POST", "/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/Currencies", payload, headers)
    res = conn.getresponse()
    data = res.read()
    res_data = json.loads(data)
    # print(res_data)
    for i in res_data["instruments"]:
        if ticker in i["name"]:
            return i["figi"]
    return None


def make_ssl():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context