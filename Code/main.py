
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