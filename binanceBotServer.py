#-*-coding:utf-8 -*-
import ccxt
import time
import pandas as pd
import pprint
import my_key

simpleEnDecrypt = my_key.SimpleEnDecrypt(b'ycJNAQPaDHt8iGpVJ1756CQ3O9ML_OBa0xdguOKsEs0=')


binance = ccxt.binance(config = {
    'apiKey':  simpleEnDecrypt.decrypt(my_key.binance_access),
    'secret':simpleEnDecrypt.decrypt(my_key.binance_secret),
    'enableRateLimit': True,
    'options' : {
        'defaultType' : 'future'
    }
})

#거래할 코인 티커와 심볼
Target_Coin_Ticker = "BTC/USDT"
Target_Coin_Symbol = "BTCUSDT"


#rsi 지표 가져오는 함수
#RSI지표 수치를 구해준다. 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def GetRSI(ohlcv,period,st):
    ohlcv["close"] = ohlcv["close"]
    delta = ohlcv["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return float(pd.Series(100 - (100 / (1 + RS)), name="RSI").iloc[st])