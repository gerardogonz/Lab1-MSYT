import pandas as pd
import numpy as np
import yfinance as yf

def precios(tickers,start_date, end_date, fechas_consulta):
    matriz = yf.download(tickers, start = start_date, end = end_date)['Close'] 
    serie_MXN = yf.download("MXN=X",start = start_date,end = end_date)["Close"]
    MXN = pd.DataFrame(data = serie_MXN)
    mxn_consulta = np.zeros(len(fechas_consulta))
    matriz_sal = []
    for i in range(len(fechas_consulta)):
        mxn_consulta[i] = MXN.loc[fechas_consulta[i]]
        matriz_sal.append(matriz.loc[fechas_consulta[i]])
    output = pd.DataFrame(data = matriz_sal, index = fechas_consulta)
    output["MXN"] = mxn_consulta   
    return output


def ticker_reformat(tickers):
    new_tickers = []
    for ticker in tickers:
        if ticker == "MXN":
            pass
        elif ticker == "LIVEPOLC.1":
            new_tickers.append(ticker.replace(".","-") +".MX")
        elif ticker == "LASITEB.1":
            new_tickers.append(ticker.replace(".","-") +".MX")
        else:
            new_tickers.append(ticker.replace("*","") +".MX")
    return new_tickers