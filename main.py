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
    # sber_figi = t.get_figi("SBER")
    # candles = t.get_candles(sber_figi, "2026-03-24T13:00:00Z", "2026-03-24T15:00:00Z", "CANDLE_INTERVAL_5_MIN")
    # # print(candles)
    # for i in candles:
    #     print(i, "\n")

    figi_bond = t.get_bond_figi("RU000A0ZYLG5")
    # figi_bond = t.get_bond_figi("SIBN6P1")

    instr1 = t.get_figi("TATN")
    instr2 = t.get_figi("ROSN")

    # for i in t.get_all_bonds():
    #     print(i, "\n")

    make_img.make_chart_candles(instr1, instr2, "CANDLE_INTERVAL_HOUR") # CANDLE_INTERVAL_1_MIN, CANDLE_INTERVAL_5_MIN, 
    # CANDLE_INTERVAL_15_MIN, CANDLE_INTERVAL_HOUR

if __name__ == "__main__":
    main()