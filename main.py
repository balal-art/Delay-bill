from locale import DAY_1
from xmlrpc.client import DateTime
import pandas as pd
from pandas.tseries.offsets import DateOffset
import datetime as dt
from datetime import datetime, timedelta
import jdatetime
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px



import numpy as np  
import sys

sys.__stdout__ = sys.stdout



class FaDict:

    sharh = 'شرح'
    karkard = 'کارکرد'
    kholaseh = 'خلاصه'
    date0 = 'تاریخ تحویل زمین :'
    mablagh0 = 'مبلغ اولیه پیمان : '
    modat0 = 'مدت اولیه پیمان : '
    date_now = 'تاریخ رسیدگی :'
    type ='نوع'
    num ='شماره'
    mablagh = 'مبلغ تجمعی'
    date_darkhast = 'تاریخ درخواست'
    date_pardakht = 'تاریخ پرداخت'
    date_tamdid = 'تاریخ شروع تمدید'
    doreh = 'دوره صورت وضعیت'
    modat_mojaz = 'مدت مجاز پرداخت'
    modat_tamdid = 'مدت تمدید پیمان'
    date_mojaz_pardakht = 'تاریخ پرداخت طبق پیمان'
    modat_takhir_pardakht = 'تاخیر در پرداخت'
    soratvazeait = 'صورت وضعیت'
    tadil = 'تعدیل'

class PymanData :

    date0 = pd.Timestamp('2020-10-28')
    mablagh0 = int(1000000000)
    modat0 = round(18*365/12) # 18 month to day
    now = pd.Timestamp.now()

mystr = FaDict
dataA = PymanData

colItem = [mystr.type, mystr.num, mystr.mablagh, mystr.date_darkhast, mystr.date_pardakht ]
dtypeItem = {mystr.num :str, mystr.num:str}

data = pd.read_excel('test.xls', sheet_name=mystr.karkard, usecols= colItem, dtype= dtypeItem,
    converters= {mystr.date_darkhast: pd.to_datetime, mystr.date_pardakht: pd.to_datetime})
data[mystr.sharh] = data[mystr.type] + ' ' + data[mystr.num]
dataPaeh = pd.read_excel('test.xls', sheet_name=mystr.kholaseh, header=None)
# print(dataPaeh)
dataA.date0 = dataPaeh.loc[(dataPaeh[0]== mystr.date0), 0:1].iat[0,1]
dataA.mablagh0 = dataPaeh.loc[(dataPaeh[0]== mystr.mablagh0), 0:1].iat[0,1]
dataA.modat0 = dataPaeh.loc[(dataPaeh[0]== mystr.modat0), 0:1].iat[0,1]
dataA.now = dataPaeh.loc[(dataPaeh[0]== mystr.date_now), 0:1].iat[0,1]
# print(dataA.date0)
# print(dataA.mablagh0)
# print(dataA.modat0)

def movaghat_furmol(modat0, mablagh0, karkard, D_darkhast, D_pardakht, T_doreh):
    T_mojaz = 20
    if T_doreh > 30 :
        T_mojaz = round(T_doreh*2/3)
    D_mojaz = D_darkhast.date() + timedelta(days=T_mojaz) #DateOffset(days=T_mojaz)
    T_takhir = (D_pardakht.date() - D_mojaz).days
    if T_takhir < 0 : T_takhir = 0
    T_tamdid = round((karkard / T_doreh) * (modat0 / mablagh0) * T_takhir * (0.697))
    D_start_takhir = (D_pardakht.date() - timedelta(days=T_tamdid))
    out_Dict = {
        mystr.date_darkhast: 22222, #D_darkhast.date(),
        mystr.doreh:T_doreh,
        mystr.modat_mojaz:T_mojaz,
        mystr.date_mojaz_pardakht:D_mojaz,
        mystr.date_pardakht:D_pardakht.date(),
        mystr.modat_takhir_pardakht:T_takhir,
        mystr.modat_tamdid:T_tamdid,
        mystr.date_tamdid:D_start_takhir
        }
    # print(out_Dict)
    return out_Dict

def movaghat(data_in, type = mystr.soratvazeait, date0=dataA.date0):
    sortIndex = mystr.num
    df = data_in.loc[(data_in[mystr.type] == type ) , :]
    df = df.loc[data_in[mystr.num]!= 'ق' , :]
    df.sort_values(by=[mystr.num])
    df[mystr.karkard] = df[mystr.mablagh] - df[mystr.mablagh].shift(periods=1, fill_value=0)  
    df[mystr.doreh] = (df[mystr.date_darkhast] - df[mystr.date_darkhast].shift(periods=1, fill_value=date0)).astype('timedelta64[D]')
    df[mystr.modat_mojaz] = pd.NA
    df[mystr.date_mojaz_pardakht] = pd.NA
    df[mystr.modat_takhir_pardakht] = pd.NA
    df[mystr.modat_tamdid] = pd.NA
    df[mystr.date_tamdid] = pd.NA

    for index, row in df.iterrows():
        # data_tmp = movaghat_furmol(df.loc[index])
        karkard = df.at[index, mystr.karkard]
        D_darkhast = df.at[index, mystr.date_darkhast]
        D_pardakht = df.at[index, mystr.date_pardakht]
        T_doreh = df.at[index, mystr.doreh]
        data_tmp = movaghat_furmol(dataA.modat0, dataA.mablagh0, karkard, D_darkhast, D_pardakht, T_doreh)
        df.at[index, mystr.modat_mojaz]= data_tmp[mystr.modat_mojaz]
        df.at[index, mystr.date_mojaz_pardakht] = data_tmp[mystr.date_mojaz_pardakht]
        df.at[index, mystr.modat_takhir_pardakht] = data_tmp[mystr.modat_takhir_pardakht]
        df.at[index, mystr.modat_tamdid] = data_tmp[mystr.modat_tamdid]
        df.at[index, mystr.date_tamdid] = data_tmp[mystr.date_tamdid]

    # print('--------------------------')
    # print(type + ' ' + 'موقت')
    # print('--------------------------')
    # print(df)
    # # print(df.dtypes)
    return df

def movaghat_overlab():
    pass




# intervalDF = pd.Interval()
frames = [movaghat(data, date0= dataA.date0),movaghat(data, type= mystr.tadil, date0=dataA.date0)]
result = pd.concat(frames)
# result.to_csv("result.csv")
# result.to_excel("result.xls", sheet_name='Sheet_name_1')
df = pd.DataFrame().assign(
                Task=result[mystr.type]+ ' ' + result[mystr.num],
                Start=result[mystr.date_tamdid],
                Finish=result[mystr.date_pardakht],
                #Complete=result[mystr.type],
                Type=result[mystr.type],
            )

# print(df)

# fig = ff.create_table(df, height_constant=60)

mytitle = 'نمودار همپوشانی تاخیر در پرداخت‌ها 5090'
# fig2 = ff.create_gantt(df, index_col='Type',
#                    show_colorbar=True, bar_width=0.5,
#                    showgrid_x=True, showgrid_y=False, title= mytitle)

fig = px.timeline(result, x_start=mystr.date_tamdid, x_end=mystr.date_pardakht, y=mystr.sharh, color=mystr.type, title= mytitle)
fig.update_yaxes(autorange="reversed")
fig.show()