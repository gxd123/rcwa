from rcwa import *
from rcwa import cscs
import numpy as np
import os

# Directory info
Dir = 'test'
Name = '1'

# Basic configurations
wavelengths = [0.633, 0.7]    # has to be in an array
periodicity = 0.7 * 0.633     # optimized for 560 nm
grat_tkn = 1
buff_tkn = 0.633
dbr_Si3N4 = 0.633 / 4.0 / 2.
dbr_SiO2  = 0.633 / 4.0 / 1.457

aspect_ratio = 6
resolution = 10

# Variables for the simulations
max_r = periodicity / 2.
min_r = grat_tkn / float(aspect_ratio) / 2.
r_list = np.linspace(min_r, max_r, num=resolution)

# Make a directory
directory = Dir + '/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Start RCWA
inputs = []
for w in wavelengths:
    for r in r_list:
        inpt = 'r-{}-({},0.),(0.,{})/TiO2={}:C(0,0,{})/SiO2={}/Ag=1.1'\
          .format(w,periodicity,periodicity,grat_tkn,r,dbr_SiO2,dbr_Si3N4)
        inputs.append(inpt)

new = RCWA(inputs, 19, field=1)
df = new.simulate()

parsed_df = cscs.parse_cscs(df, {'wl':1, 'r1':11})
avg_df = cscs.take_avg(parsed_df)
final_df = cscs.combine_colors(avg_df)

final_df.to_csv(directory + 'pillar_data.csv')
