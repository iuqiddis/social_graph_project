import dill
import pandas as pd
import numpy as np
from datetime import datetime as dt
import os

#import from dill
lnks = dill.load(open('links.pkd', 'rb'))
dun = dill.load(open('dates_un.pkd', 'rb'))
dfm = dill.load(open('dates_form.pkd', 'rb'))

ald = pd.DataFrame({'url': lnks,
                    'unf': dun,
                    'time': dfm})

#ald is all the links and time together in a dataframe
print(ald.head())


ald['year'] = ald['time'].dt.strftime("%Y")
ald['month'] = ald['time'].dt.strftime("%m")
ald['day'] = ald['time'].dt.strftime("%d")
ald['monY'] = ald['time'].dt.strftime("%b-%Y")
# did i need separate year, month and day. nope. just needed the monY column

#alf = ald[(ald['year'] <= '2014') and (ald['month'] <= '12') and (ald['day'] <= '1')]
#when you have time see if that line above works
alf = ald.query('time < 20141202')

link_list = alf['url'].tolist()
dill.dump(link_list, open('link_list_2014.pkd', 'wb'))

#print(alf.head())
print(len(link_list))

#alg = alf.groupby([(alf.time.dt.year), (alf.time.dt.month)]).count()
#check if above works as well

#alh = alf.groupby('monY') #This works
#mlc = alh.count() #month list

#print(mlc.index)

#This bit doesn't work due to some indexing error. But the thing at the bottom works
# ml = [i for i in range(0,95)]
# for i in ml:
#      ml[i] = (mlc.loc[i, 'monY'], mlc.loc[i, 'day'])



# mlc.to_csv('mlc.csv', index=True)
#
# df = pd.read_csv('mlc.csv')
# ml = [i for i in range(0,95)]
# for i in ml:
#     ml[i] = (df.loc[i, 'monY'], df.loc[i, 'day'])
# print(ml)