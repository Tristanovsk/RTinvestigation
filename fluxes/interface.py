import sys, os
import numpy as np
import pandas as pd
import glob

'''

'''


files = '/DATA/VRTC/OSOAA_profile/RESULTS/PROFILE/fluxes*'
files = glob.glob(files)
file=files[0]
name = os.path.basename(file)
df = pd.read_csv(file, skiprows=30,sep=' ',skipinitialspace=True)
df[(df.Z<0) & (df.Z>-50)].plot.scatter('Ed','Z',c='SZA',title=name)
df[(df.Z<0.01) & (df.Z>-0.0015)].plot.scatter('Eu','Z',c='SZA',title=name)

df_p=df[df.Z==0]
df_m=df[df.Z==-0.001]

eps=df_p.Ed-df_p.Eu +np.array(-df_m.Ed+df_m.Eu)