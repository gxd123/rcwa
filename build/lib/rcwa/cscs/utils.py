import pandas as pd
import numpy as np


def parse_cscs(df, position_col, drop_cscs=True):
    """
    input: (input_pd, {'column_name':'position', ...})
    return: output_pd
    """
    
    def row_to_values(row):
        """converst a row of data into a list of values"""

        new_str = row.replace('-',',').replace(')',',')\
            .replace('(',',').replace('=',',').replace('/',',').\
            replace(':',',').replace('[',',').replace(']',',').split(',')
        return [x for x in new_str if x != ''] 

    df['parsed'] = df['CSCS'].apply(row_to_values)
    
    for key, position in position_col.iteritems():
        df[key] = df['parsed'].apply(lambda cscs: cscs[position])
    
    df = df.drop(['parsed'], axis=1)
    if drop_cscs: 
        df = df.drop(['CSCS'], axis=1)
    
    return df


def take_avg(df):
    """input: df, desired output length, whether or not you want phase and intensity
    one: True when sampling 1x1 field. """
    
    output = df['e_field'].apply(lambda field: avg_field_to_phase(eval(field)))
    
    df['phase'] = [x[0] for x in output]
    df['intensity'] = [x[1] for x in output]
    df['e_field'] = [x[2] for x in output]

    return df


def avg_field_to_phase(field):
    """input the field, returns the average phase, intensity, and field """
    
    length = len(field)
    real = np.real(field)
    imag = np.imag(field)
    
    #resample the field
    real = np.mean(real)
    imag = np.mean(imag)

    # vectorize the phase function
    phaser = np.vectorize(lambda real, imag: np.arctan2(imag, real))
    intensity = np.abs(real+imag*1j)**2
    phase = phaser(real, imag)
    
    return phase.tolist(), intensity.tolist(), (real+imag*1j).tolist()
        
    
def combine_colors(new_df):
    """combine all colors together for lens maker"""
    
    wavelengths = new_df['wl'].unique()
    composite_df = new_df[new_df.wl == wavelengths[0]].copy(deep=True)
    composite_df = composite_df.drop(columns=['phase', 'intensity',\
                                               'wl', 'e_field'])
    for wl in wavelengths:
        composite_df['t_'+str(wl)] = new_df[new_df.wl == str(wl)]['intensity'].values
        composite_df['p_'+str(wl)] = new_df[new_df.wl == str(wl)]['phase'].copy().values
        composite_df['e_'+str(wl)] = new_df[new_df.wl == str(wl)]['e_field'].copy().values
    return composite_df
        
    
