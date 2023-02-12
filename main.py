
import functions as fn
import data as dt
import pandas as pd
import numpy as np

tickers, cash_tickers, pond, pond_cash = dt.tickers()

fechas_consulta=pd.to_datetime(["2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31",
        "2021-06-30","2021-07-30","2021-08-31","2021-09-30","2021-10-26",
        "2021-11-30","2021-12-31","2022-01-26","2022-02-28","2022-03-31",
        "2022-04-29","2022-05-31","2022-06-30","2022-07-29","2022-08-31",
        "2022-09-30","2022-10-31","2022-11-30","2022-12-30","2023-01-25"])

precios = fn.precios(
    fn.ticker_reformat(tickers),
    start_date=fechas_consulta[0],
    end_date="2023-01-26",
    fechas_consulta=fechas_consulta
    )


precios_cash = fn.precios(
    fn.ticker_reformat(cash_tickers),
    start_date=fechas_consulta[0],
    end_date="2023-01-26",
    fechas_consulta=fechas_consulta
)
precios_cash.drop("MXN",axis=1,inplace=True)
pasiva_inicial = fn.pasiva_inicial(precios,precios_cash,tickers,pond,pond_cash,1e6)

#### ACTIVA
tickers_activa, pond_activa = dt.tickers_activa()

precios_activa = fn.precios_activa(
    fn.ticker_reformat(tickers_activa),
    start_date="2021-01-31",
    end_date="2022-01-31"
    )
# Para desarrollo de markowitz, exportar a csv
cash_t = ["SITESB.1","NMKA"]
precios_activa.to_csv("markowitz/precios_activa.csv")

### Obteniendo ponderación del cash
temp = []
for t in cash_t:
    temp.append(pond_activa.loc[t][0])
cash_activa = pd.DataFrame(columns=["Ticker","Pond"])
cash_activa["Ticker"] = cash_t
cash_activa["Pond"] = temp
pond_activa.drop(cash_t,inplace = True)

## Obtención de los precios de los activos para evaluar la estrategia
precios_activa_estrategia = fn.precios_activa(
    fn.ticker_reformat(tickers_activa),
    start_date="2022-01-31",
    end_date="2023-01-31"
    )

##### Obtención del portafolio Eficiente en Media Varianza (EMV), portafolio inicial
price_data = pd.read_csv("markowitz/precios_activa.csv",index_col=0)
price_data = price_data.drop(columns=["SITESB-1.MX","NMKA.MX"])
price_data = price_data.replace(0,np.nan)
corr = price_data.corr()
annual_ret_sum =  fn.mean_var_generator(price_data)
w, emv = fn.port_EMV(annual_ret_sum,corr,0.05)

## Corrección de los tickers
precios_activa_estrategia = precios_activa_estrategia.drop(columns=["SITESB-1.MX","NMKA.MX"])
precios_activa_estrategia = precios_activa_estrategia.replace(0,np.nan)


#### Ejecución de la estrategia

#y, z = fn.rebalanceo(precios_activa_estrategia,w,1e6,0.1/100)
inversion_activa = fn.rebalanceo(precios_activa_estrategia,w,1e6,0.1/100)

