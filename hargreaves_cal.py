
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


data = pd.read_csv('min_temp.csv')
ds = pd.read_csv('max_temp.csv')
RH = pd.read_excel('RELATIVE HUMIDITY.xlsx')

rnett =  pd.read_csv("net_Radiation.csv")
rnett.drop('Unnamed: 0', axis =1)
rnett['Date [annual]'] = pd.DatetimeIndex(rnett['Date [annual]'])
rnett = rnett.set_index('Date [annual]')
RH['Time[h]'] = pd.DatetimeIndex(RH['Time[h]'])
rnett = rnett.resample('H').mean()

new_data = pd.read_csv('new_data.csv')
new_data.drop('Unnamed: 0', axis =1)
new_data['TIME'] = pd.DatetimeIndex(new_data['TIME'])
new_data = new_data.set_index('TIME')
RH= RH.set_index(RH['Time[h]'])
new_data = new_data.resample('H').mean()
RH = RH.resample('H').mean()

T = data['T (Celcius)']
Rnet = rnett.RNet
# RNet_drop = Rnet 
# RNet = RNet_drop


T = new_data['T (Celcius)']
Tx = ds.C
Tn = data['T (Celcius)']


lamb = []
for i, item in enumerate(T):
    l = (2.501 - (0.0236 * T[i]))
    lamb.append(l)
    
def Hargreaves(T, Tx, Tn, RNet, lamb):
    h = 0.0023*((T + 17.8)*(Tx - Tn)**0.05)* RNet / (lamb)
    return h

H=[]
for i,item in enumerate(Tx):
#     print(item)
    h =(Hargreaves(T[i],Tx[i],Tn[i],Rnet[i], lamb[i]))
    H.append(h)
    

# df = df.set_index('Date')
# df.plot()

# df2 = df.resample('1D').mean()
# df2.plot()

# df3 = df.resample('M').mean()
# df3.plot()

slope = []
for i ,item in enumerate(T):
    s = 4098 * (0.6108 * math.exp((17.27 * T[i])/(T[i] + 237.3))) / ((T[i] + 237.3)**2)
    slope.append(s)
    
ES =[]
for i, item in enumerate (T):
    es = 0.611 ** (17.27 * T[i]) / (T[i] + 273.3)
    ES.append(es)
    
    
EN=[]
for i, item in enumerate(rh):
    en = (rh[i] * ES[i]) / 100
    EN.append(en)
    
# psyco = 0.06734878007
psyco = 0.054
alpha = 1.3

def pt (slope, rnet, lamb, T):
    p = alpha * (slope / (slope + psyco)) * (rnet / lamb)
    return p

PT = []
for i, item in enumerate(T):
    p = (pt(slope[i], Rnet[i], lamb[i], T[i]))
    p = p/10
    PT.append(p)
    

df = pd.DataFrame(H , columns=['Hargreaves'])
date = pd.date_range(start='2013-01-01 00:00:00' , end ='2013-12-31 23:00:00', periods = 8760)
df = df.assign(Date=date)
df = df.assign(Presly_Taylor=PT)


df = df.set_index('Date')
# plt.plot(df.index, df.Hargreaves)
# plt.plot(df.index, df.Presly_Taylor)

df2 = df.resample('1H').mean()
plt.plot(df2.index, df2.Hargreaves)
plt.plot(df2.index, df2.Presly_Taylor)

# df3 = df.resample('M').mean()
# df3.plot()

a= [1, 4, 5, 6]
sum = 0
for i, item in enumerate(a):
    sum  += item 
    
pw = 997.77



LE = rnett['LE']

sum1 = 0
ET = []
for i, item in enumerate(lamb):
    a =  1/pw 
    sum1 =+ (LE[i] / lamb[i])
    # sum1 += sum1
    # E = a * sum1
    # print(sum1)
    ET.append(sum1)





ec = pd.DataFrame(ET , columns=['Eddy_Cov'])
df = df.assign(Eddy_Cov=ec)

df2 = df.resample('1D').mean()






plt.plot(df2.index, df2.Hargreaves)
plt.plot(df2.index, df2.Presly_Taylor)
plt.plot(df2.index, df2.Eddy_Cov)















