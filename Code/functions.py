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


def pasiva_inicial(precios, precios_cash, tickers, pond, cash_pond, c_0):
    # Cálculo de inversión de acuerdo a ponderación y redondeo
    precios_0 = np.array(precios.iloc[0,:])
    precios_cash_0 = np.array(precios_cash.iloc[0,:])
    pos_inic_money = np.multiply(np.array(pond)/100,c_0)
    pos_inic_cash_money = np.multiply(np.array(cash_pond)/100,c_0)
    pos_inic = []
    for i in range(len(precios_0)):
        pos_inic.append(
            pos_inic_money[i]/precios_0[i]
        )
    pos_inic = np.array(pos_inic)
    pos_inic_floor = np.floor(pos_inic)
    cash = np.multiply(pos_inic,precios_0).sum() - np.multiply(pos_inic_floor,precios_0).sum()
    cash += pos_inic_cash_money.sum()
    out = pd.DataFrame(columns= ["Ticker","Peso(%)","Precio","Acciones","Total"])
    out["Ticker"] = tickers
    out["Peso(%)"] = pond
    out["Precio"] = precios_0
    out["Acciones"] = pos_inic_floor
    out["Total"] = out["Precio"]*out["Acciones"]
    out.loc["Cash"] = ["Cash",(cash/c_0)*100,cash,1,cash]
    return out, cash

def inversion_pasiva(inicial,precios,comision,cash,fechas_consulta):
    out = pd.DataFrame(columns=["Fecha","Portafolio","Rend","Acum"])
    out["Fecha"] = fechas_consulta
    acciones = np.array(inicial["Acciones"][:-1])
    invest = precios*acciones
    temp = []
    for i in range(len(fechas_consulta)):
        temp.append(invest.iloc[i].sum()+cash)
    out["Portafolio"] = temp
    out["Rend"] = out["Portafolio"].pct_change()
    out["Acum"] = out["Rend"].cumsum()
    out["Portafolio"][0] = 1e6
    return out.round(2)