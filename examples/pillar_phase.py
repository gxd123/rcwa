from rcwa import *
from rcwa.cscs import *
import numpy as np
import os


Dir = 'test'
Name = '1'


# configuration
wavelengths = [0.633] # has to be in an array
periodicity = 0.7*0.633 # optimized for 560 nm
grat_tkn = 1
buff_tkn = 0.633
dbr_Si3N4 = 0.633 / 4.0 / 2.
dbr_SiO2  = 0.633 / 4.0 / 1.457

aspect_ratio = 6
resolution = 300


# don't worry about
max_r = periodicity/2.
min_r = grat_tkn/float(aspect_ratio)/2.
r_list = np.linspace(min_r, max_r, num=resolution)


# make a directory
directory = Dir + '/'
if not os.path.exists(directory):
    os.makedirs(directory)

subdivision = 1



# start RCWA
inputs = []
for w in wavelengths:
    for r in r_list:
        inpt = 'r-{}-({},0.),(0.,{})/TiO2={}:C(0,0,{})/SiO2={}/Ag=1.1'\
          .format(w,periodicity,periodicity,grat_tkn,r,dbr_SiO2,dbr_Si3N4)
        inputs.append(inpt)


new = RCWA(inputs, 19, field=1)
df = new.simulate()

df.to_csv(directory+Name+'.csv', index=False)


# all this converts the RCWA E_Fields to phase and amplitude

df_og = pd.read_csv(directory+Name+'.csv', engine = 'c')

df = uppack_CSCS(df_og)
df = extract_features(df, subdivision=subdivision, n_r = 1)
df = df.drop(columns=['e_field','CSCS'])

df_unq = df[df.wavelength == wavelengths[0]].copy(deep=True)
df_unq = df_unq.drop(columns = ['p_avg', 't_avg', 'wavelength'])

for wl in wavelengths:
    df_unq['p_'+str(wl)] = df[np.isclose(df.wavelength, wl)].p_avg.tolist()
    df_unq['t_'+str(wl)] = df[np.isclose(df.wavelength, wl)].t_avg.tolist()

df_unq.to_csv(directory+Name+'_sub' + str(subdivision) + '.csv', index=False)



df = pd.read_csv(directory+Name+'_sub' + str(subdivision) + '.csv', engine= 'c', delimiter=',', encoding="utf-8-sig")
new_df = df.copy()

for wl in wavelengths:
    new_df['p_'+str(wl)] = new_df['p_'+str(wl)].apply(lambda x: eval(x)[0]/(6.28))
    new_df['t_'+str(wl)] = new_df['t_'+str(wl)].apply(lambda x: eval(x)[0])

    lines = new_df.plot.line(x='r1', y=['p_'+str(wl), 't_'+str(wl)])
