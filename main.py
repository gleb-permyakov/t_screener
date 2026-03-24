import os
import http.client
import json
import ssl
from dotenv import load_dotenv

import t
import make_img

load_dotenv()
TOKEN = os.environ.get("TOKEN")

def main():
    figi_bond1 = t.get_bond_figi("RU000A102YG7")
    figi_bond2 = t.get_bond_figi("RU000A1069P3")

    instr1 = t.get_figi("PLZL")
    instr2 = t.get_figi("MAGN")

    usd_figi = t.get_currency_figi_by_name("Доллар США")
    aur_figi = t.get_currency_figi_by_name("Золото")
    ser_figi = t.get_currency_figi_by_name("Серебро")

    make_img.make_chart_candles(instr2, usd_figi, "CANDLE_INTERVAL_WEEK") # CANDLE_INTERVAL_1_MIN, CANDLE_INTERVAL_5_MIN, 
    # CANDLE_INTERVAL_15_MIN, CANDLE_INTERVAL_HOUR,CANDLE_INTERVAL_4_HOUR,  CANDLE_INTERVAL_WEEK

if __name__ == "__main__":
    main()