"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py :                          -- #
# -- author:                                                                        -- #
# -- license:                                                                            -- #
# -- repository:                                                                      -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd


def tickers():
    df = pd.read_csv('files/NAFTRAC_20210129.csv',skiprows=2)
    df2 = pd.read_csv('files/NAFTRAC_20210226.csv',skiprows=2)
    df3 = pd.read_csv('files/NAFTRAC_20210331.csv',skiprows=2)
    df4 = pd.read_csv('files/NAFTRAC_20210430.csv',skiprows=2)
    df5 = pd.read_csv('files/NAFTRAC_20210531.csv',skiprows=2)
    df6 = pd.read_csv('files/NAFTRAC_20210630.csv',skiprows=2)
    df7 = pd.read_csv('files/NAFTRAC_20210730.csv',skiprows=2)
    df8 = pd.read_csv('files/NAFTRAC_20210831.csv',skiprows=2)
    df9 = pd.read_csv('files/NAFTRAC_20210930.csv',skiprows=2)
    df10 = pd.read_csv('files/NAFTRAC_20211026.csv',skiprows=2)
    df11 = pd.read_csv('files/NAFTRAC_20211130.csv',skiprows=2)
    df12 = pd.read_csv('files/NAFTRAC_20211231.csv',skiprows=2)
    df13 = pd.read_csv('files/NAFTRAC_20220126.csv',skiprows=2)
    df14 = pd.read_csv('files/NAFTRAC_20220228.csv',skiprows=2)
    df15 = pd.read_csv('files/NAFTRAC_20220331.csv',skiprows=2)
    df16 = pd.read_csv('files/NAFTRAC_20220429.csv',skiprows=2)
    df17 = pd.read_csv('files/NAFTRAC_20220531.csv',skiprows=2)
    df18 = pd.read_csv('files/NAFTRAC_20220630.csv',skiprows=2)
    df19 = pd.read_csv('files/NAFTRAC_20220729.csv',skiprows=2)
    df20 = pd.read_csv('files/NAFTRAC_20220831.csv',skiprows=2)
    df21 = pd.read_csv('files/NAFTRAC_20220930.csv',skiprows=2)
    df22 = pd.read_csv('files/NAFTRAC_20221031.csv',skiprows=2)
    df23 = pd.read_csv('files/NAFTRAC_20221130.csv',skiprows=2)
    df24 = pd.read_csv('files/NAFTRAC_20221230.csv',skiprows=2)
    df25 = pd.read_csv('files/NAFTRAC_20230125.csv',skiprows=2)

    x= pd.concat([df, df2, df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20,df21,
                                df22,df23,df24,df25], axis=0).drop(37) 

    group = x.groupby(["Ticker"])
    count = group["Ticker"].count().to_frame()
    tickers= count[count['Ticker'] == 25]
    cash_tickers = count[count["Ticker"] != 25]
    output = list(tickers.index)
    output_cash_dirty = list(cash_tickers.index)
    output_cash = []
    pond = []
    pond_cash = []
    for ticker in output:
        pond.append(df25["Peso (%)"][df25["Ticker"] == ticker].to_numpy()[0])
    for ticker in output_cash_dirty:
        if df25["Peso (%)"][df25["Ticker"] == ticker].values > 0:
            pond_cash.append(df25["Peso (%)"][df25["Ticker"] == ticker].values)  
            output_cash.append(ticker) 
        else:
            pass 
    return output, output_cash, pond, pond_cash

def tickers_activa():
    df = pd.read_csv('files/NAFTRAC_20210129.csv',skiprows=2)
    tickers = pd.unique(df["Ticker"])[:-1]
    pond = pd.DataFrame(columns=["Ticker","Pond"])
    pond["Ticker"] = tickers
    temp = []
    for ticker in tickers:
        temp.append(df["Peso (%)"][df["Ticker"] == ticker].to_numpy()[0])
    pond["Pond"] = temp
    pond.set_index("Ticker",inplace=True)

    return tickers, pond
