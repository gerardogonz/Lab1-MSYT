"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize


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
        elif ticker == "SITESB.1":
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

def precios_activa(tickers,start_date, end_date):
    data = yf.download(tickers, start = start_date, end = end_date)['Close'] 
    serie_MXN = yf.download("MXN=X",start = start_date,end = end_date)["Close"]
    data.reset_index(inplace=True)
    newcol = data["Date"].dt.tz_localize(None)
    data["Date"] = newcol
    data.set_index("Date",inplace=True)
    mxn_consulta = np.zeros(len(newcol))
    MXN = pd.DataFrame(data = serie_MXN)
    for i in range(len(newcol)):
        mxn_consulta[i] = MXN.loc[newcol[i]]
    data["MXN"] = mxn_consulta
    return data 

def sharpe():
    pass

def activa_inicial(precios, tickers, pond, cash_pond, c_0):
    # Cálculo de inversión de acuerdo a ponderación y redondeo
    precios_0 = np.array(precios.iloc[0,:])
    pos_inic_money = np.multiply(np.array(pond["Pond"])/100,c_0)
    pos_inic_cash = np.array([i/100*c_0 for i in cash_pond["Pond"]]).sum()
    pass

## Implement a function that optimizes a portfolio of stocks using the Markowitz model

def mean_var_generator(price_timeseries):
    anual_ret_summ = pd.DataFrame(columns=price_timeseries.columns,index=["Mean","Std"])
    for i in price_timeseries.columns:
        anual_ret_summ[i]["Mean"] = price_timeseries[i].mean()
        anual_ret_summ[i]["Std"] = price_timeseries[i].std()
    
    return anual_ret_summ

def port_EMV(annual_ret_summ,corr,rf):
    ## Construcción de parámetros
    # 1. Sigma: matriz de varianza-covarianza Sigma = S.dot(corr).dot(S)
    S = np.diag(annual_ret_summ.loc['Std'].values)
    Sigma = S.dot(corr).dot(S)
    # 2. Eind: rendimientos esperados activos individuales
    Eind = annual_ret_summ.loc['Mean'].values
    # Función objetivo
    # Función objetivo
    def menos_RS(w, Eind, Sigma, rf):
        Ep = Eind.T.dot(w)
        sp = (w.T.dot(Sigma).dot(w)) ** 0.5
        RS = (Ep- rf) / sp
        return -RS
    n = len(Eind)
    # Número de activos
    n = len(Eind)
    # Dato inicial
    w0 = np.ones((n,)) / n
    # Cotas de las variables
    bnds =((0,1),) * n
    # Restricciones
    cons = {'type': 'eq', 'fun': lambda w: w.sum() - 1}
    # Portafolio EMV
    EMV = minimize(fun = menos_RS,
                x0 = w0,
                args = (Eind, Sigma, rf),
                bounds = bnds,
                constraints = cons,
                tol = 1e-8)
    w_EMV = EMV.x
    w_EMV = w_EMV.round(4)
    # Pesos, rendimiento y riesgo del portafolio EMV
    E_EMV = Eind.T.dot(w_EMV)
    s_EMV = (w_EMV.T.dot(Sigma).dot(w_EMV)) ** 0.5
    RS_EMV = (E_EMV - rf) / s_EMV
    return w_EMV, [E_EMV, s_EMV, RS_EMV]


## Implementación de una función, que dados los pesos 
# de un portafolio, y dadas las siguientes condiciones:
# Disminuir en 2.5% la posición en activos cuyo precio disminuyó un 5% o más
# Aumentar en 2.5% la posición en activos cuyo precio aumentó un 5% o más
# Considera el pago de comisiones de 0.1% por operación
def rebalanceo(precios, pesos, capital_inicial , comision):
    # Eliminando todos los precios y pesos que sean 0
    remain = []
    new_pesos = []
    for i in range(len(pesos)):
        if pesos[i] != 0:
            remain.append(precios.columns[i])
            new_pesos.append(pesos[i])
    precios = precios[remain] 
    pesos = np.array(new_pesos)
    # 1. Aplicar comisión al capital inicial
    capital_inicial *= (1 - comision)
    # 2. Calcular rendimientos
    rend = precios.pct_change()
    # 3. Calcular posición inicial
    pos_inic = np.multiply(pesos,capital_inicial)
    # 4. Calcular evolución del portafolio
    pesos_inic = np.repeat(pos_inic.reshape(1,len(pesos)),len(rend)+1,axis=0)
    precio_0 = precios.iloc[0,:]
    print(precio_0)
    titulos_0 = (precio_0/pesos)/100
    print(titulos_0)
    titulos_0 = titulos_0.sum()
    print(titulos_0)
    titulos_compra = []
    titulos_compra.append(np.floor(titulos_0))
    for i in range(len(rend)):
        for j in range(len(pesos)):
            if rend.iloc[i,j] >= 0.05:
                pesos_inic[i+1,j] = pesos_inic[i,j] * 1.025
                temp = pesos_inic[i+1,j] / precio_0[j]
                temp = temp.sum()
                titulos_compra.append(np.floor(temp))
                titulos_0 = temp
            elif rend.iloc[i,j] <= -0.05:
                pesos_inic[i+1,j] = pesos_inic[i,j] * 0.975
                temp = pesos_inic[i+1,j] / precio_0[j]
                temp = temp.sum()
                titulos_compra.append(np.floor(-temp))
                titulos_0 = temp
            else:
                pesos_inic[i+1,j] = pesos_inic[i,j]
    portafolio = pesos_inic.sum(axis=1)
    # 5. Calcular rendimientos y acumulados
    # Calcular el rendimiento (cambio porcentual) del portafolio, es un numpy array
    rend_portafolio = pd.DataFrame(portafolio,columns=["rend"]).pct_change()

    portafolio = pd.DataFrame({
        "Portafolio": portafolio,
        "Rend": rend_portafolio["rend"],
        "Acum": rend_portafolio["rend"].cumsum()
    })
    # Calculamos el histórico de operaciones
    titulos_totales = np.array(titulos_compra).cumsum()
    comisiones = np.abs(np.array(titulos_compra)) * comision    
    comision_acum = comisiones.cumsum()
    # Armando el registro de operaciones
    operaciones = pd.DataFrame({
        "Titulos totales": titulos_totales,
        "Titulos comprados": titulos_compra,
        "Comisión": comisiones,
        "Comisiones acumuladas": comision_acum})
    return portafolio.round(2), operaciones

def evaluacion_des(pasiva,activa,rf):
    matriz = np.array([
        [pasiva["Rend"].mean()*252/12, activa["Rend"].mean()*252/12],
        [pasiva["Rend"].std()*252**0.5, activa["Rend"].std()*252**0.5],
        [pasiva["Acum"][pasiva.index[-1]]*252/12, activa["Rend"][activa.index[-1]]*252/12]
    ])
    matriz_2 = np.array([
        [matriz[0,0], matriz[0,1]],
        [matriz[2,0], matriz[2,1]],
        [(matriz[0,0]-rf)/matriz[1,0], (matriz[0,1]-rf)/matriz[1,1]]
        ])
    df = pd.DataFrame(columns=["Descripción","Pasiva","Activa"],
    index=["rend_m","rend_c","Sharpe"])    
    df["Descripción"] = ["Rendimiento promedio mensual","Rendimiento mensual acumulado","Sharpe"]
    df["Pasiva"] = matriz_2[:,0]
    df["Activa"] = matriz_2[:,1]
    return df.round(2)

    



