import sys, os
import numpy as np
import plotly.offline as po
import pandas as pd

import datetime
import glob

'''

'''

cmap = 'viridis'
files = '/DATA/VRTC/OSOAA_profile/RESULTS/PROFILE/fluxes*chl0.03_sed0.00'
files = glob.glob(files)
files.sort()

def info2dict(info):
    '''convert information content from first line (command line) of the LUT files
       into dict object'''
    info = info.split('-')
    metadata = {}
    yep = 1
    for info_ in info[1:-1]:
        info_ = info_.split()
        try:
            if yep == 0:
                metadata[meta_prev] = '-' + info_[0]
            else:
                metadata[info_[0]] = info_[1]
            yep = 1
        except:
            meta_prev = info_[0]
            yep = 0

    return metadata


df = pd.DataFrame()
for file in files:
    mdate = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    if mdate.year < 2018:
        print(file, mdate)
        pass
    name = os.path.basename(file)
    info = pd.read_csv(file, nrows=1, header=None)[0][0]
    metadata = info2dict(info)

    df_ = pd.read_csv(file, skiprows=31, sep=' ', skipinitialspace=True)
    for key, val in zip(metadata.keys(), metadata.values()):
        print(key, val)
        df_[key] = val
    df = df.append(df_)

df[(df.Z < 100000) & (df.Z >= 0)].plot.scatter('Ed', 'Z', c='SZA', colormap=cmap, title=name)
df[(df.Z < 0) & (df.Z > -10)].plot.scatter('Eo', 'Z', c='c', colormap=cmap, title=name,logx=True)

df[(df.Z < 0.01) & (df.Z > -0.0015)].plot.scatter('Eu', 'Z', c='SZA', colormap=cmap, title=name)

df_p = df[df.Z == 0]
df_m = df[df.Z == -0.001]

df_p = df[df.LEVEL == 76]
df_m = df[df.LEVEL == 77]

df_ = df[df.LEVEL == 80]
df_['eps'] = np.array(df_p.Ed - df_p.Eu + np.array(-df_m.Ed + df_m.Eu))
df_['wl'] = np.array(df_m['OSOAA.Wa'], dtype=np.float) * 1000
df_['c_over_a']= df_.c/(df_.aw+df_.achl+df_.amin+ df_.acdom)
df_[['eps', 'SZA', 'wl', 'c']].plot.scatter(x='SZA', y='eps', c='c', colormap=cmap)
#df_=df_[df_.achl < 10]
fig = {
    'data': [
  		{
        'x': df_.SZA,
        'y': df_.eps,
        'text':df_.wl,
        'mode': 'markers',
        'marker':dict(
        size=16,
        color = df_.c_over_a, #set color equal to a variable
        colorscale='Viridis',
        showscale=True)},

    ],
    'layout': {
        'xaxis': {'title': 'SZA'},
        'yaxis': {'title': 'eps'}
    }
}

po.plot(fig)