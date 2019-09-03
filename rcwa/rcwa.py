# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = "Luocheng Huang"
__copyright__ = "Copyright 2018"
__credits__ = ["Luocheng Huang"]
__license__ = "GPL"
__version__ = "0.2.0"
__maintainer__ = "Luocheng Huang"
__email__ = "luocheng@uw.edu"
__status__ = "Production"


import S4
import pandas as pd
import os
import numpy as np
import math
import time as time
from multiprocessing import Pool
from os.path import join as pjoin
import matplotlib.pyplot as plt
import re


dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_cscs(df, position_col):
    """
    input: (input_pd, {'column_name':'position', ...})
    return: output_pd
    """

    def row_to_values(row):
        """converst a row of data into a list of values"""

        new_str = row.replace('-',',').replace(')',',')\
            .replace('(',',').replace('=',',').replace('/',',').\
            replace(':',',').split(',')
        return [x for x in new_str if x != '']

    df['CSCS'] = df['CSCS'].apply(row_to_values)

    for key, position in position_col.iteritems():
        df[key] = df['CSCS'].apply(lambda cscs: cscs[position])

    df = df.drop(columns=['CSCS'])

    return df


def simulate_one(config, field=1):
    """a wrapper for pickling
    simulates one instance
    """
    global FIELD
    FIELD = field
    new = RCWA.Simulation(Nxy=RCWA.Nxy)
    new.load_input(config)
    return new.run()


class RCWA(object):
    """
    An rcwa simulation ojbect
    """


    def __init__(self, input_list=None, cores=10, field = None, Nxy=52):
        self.input = input_list
        self.cores = cores
        self.field = field
        self.Nxy = Nxy
        global FIELD
        """field is the amount of field in the center measured. 1 is 100% .5 is 25%
            returns the mean value if field==None
            else returns the center field."""
        FIELD = field
        pass


    def timeit(method):
        """a decor for timing methods, should be used as a decorator
        """
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            if 'log_time' in kw:
                name = kw.get('log_name', method.__name__.upper())
                kw['log_time'][name] = int((te - ts) * 1000)
            else:
                print '%r  %2.2f s' % \
                      (method.__name__, (te - ts) )
            return result
        return timed


    @timeit
    def simulate_and_graph(self):
        """
        inputs the attribute list,
        :return: simulate results
        """

        p = Pool(self.cores)
        df = pd.DataFrame()
        FIELD = self.field
        solution = p.map(simulate_one, self.input)  # create a pool of workers and map it onto different cores
        p.close() # prevent memory leakage
        p.join() # synchronization point

        t_list = []
        p_list = []
        for s in solution:
            t_list.append(s[0])
            p_list.append(s[1])
        # make phase continuous
        # new_p = unwrap(p_list)
        new_p = [x[0] / (2*math.pi) for x in p_list]

        config = self.input[0]

        # plot data
        plt.figure(0)
        plt.figure(figsize=(10, 5), dpi=200)
        label1 = 'phase'
        label2 = 'amplitude'
        plt.plot(new_p, label=label1)
        plt.plot(t_list, label=label2)
        plt.xlabel('Grating post width')
        plt.ylabel('amp & phase')
        plt.title('Wavelength = {} nm'.format('unknown'))
        plt.legend()


        plt.savefig("{}.png".format(('unknown')))
        plt.show();
        plt.clf();

        # save to csv
        a = (new_p, t_list)

        np.savetxt("data_{}.csv".format(('unknown')), a, delimiter=",")


        pass


    @timeit
    def simulate(self, debug=False):
        """
        inputs the attribute list,
        :return: simulate results
        """

        p = Pool(self.cores)
        df = pd.DataFrame(self.input)
        # create a pool of workers and map it onto different cores
        if debug:
            solution = map(simulate_one, self.input)
        else:
            solution = p.map(simulate_one, self.input)
        solutions = pd.DataFrame(solution)
        p.close() # prevent memory leakage
        p.join() # synchronization point

        result = pd.concat([df, solutions], axis=1)
        result.columns = ['CSCS', 'e_field']

        # make phase continuous
        # new_p = unwrap(p_list)

        return result


    class Simulation:
        """A simulation object"""

        def __init__(self, Nxy='default'):
            self.layers = []
            self.basis = ((1,0),(0,1))
            self.NumBasis=150
            self.layers = None
            self.layer_material = None
            self.layer_thickness = None
            self.layer_pattern = None
            self.transmission = None
            self.wavelength = None
            self.buffer = 0.1
            self.Nxy = Nxy
            if self.Nxy == 'default':
                raise ValueError, 'Nxy not given'


        def load_input(self,input_instance):
            """loades the canonical id into local variables"""

            # the first step is to assign values to the variables from the
            # input_instance
            parts = input_instance.split('/')
            first_arg = parts[0].split('-')
            if first_arg[0] == 't':
                self.transmission = True
            elif first_arg[0] == 'r':
                self.transmission = False

            self.wavelength = float(first_arg[1])
            self.basis = eval(first_arg[2])

            self.layers = parts[1:]
            layers_split = [layer.split('=') for layer in self.layers]
            self.layer_material = [layer_split[0] for layer_split in layers_split]
            # split_2 is everything after the '=' for each layer
            split_2 = [layer_split[1] for layer_split in layers_split]
            self.layer_thickness = []
            self.layer_pattern = []
            for x in split_2:
                x_split = x.split(':')
                if len(x_split) == 1:
                    # if there's only 1 number that means a homogenous layer
                    self.layer_thickness.append(float(x_split[0]))
                    self.layer_pattern.append(None)
                else:
                    # if there's one or multiple shapes
                    self.layer_thickness.append(float(x_split[0]))
                    self.layer_pattern.append(':'.join(x_split[1:]).split('+'))


        def run(self):
            """create layers and return a S4 object
            :type attr: dict
            return S
            """
            def querry_n(material, wavelength):
                """
                given the material in string, wavelength in µm
                output (n,k)
                if given a list then return the first part as n, second part as k*j.
                """

                try:
                    input_list = eval(material)

                    if type(input_list) != list:
                        raise Exception('Please use format: [n, k] for the matierla.')
                    if len(input_list) != 2:
                        raise Exception('Did you include k? Please use format: [n, k] for the material!')

                    n = input_list[0]
                    k = 1j*input_list[1]

                except:

                    try:
                        mat = pd.read_csv(pjoin(dir_path,'data','n_data','{}_n.csv'.format(material)))
                    except:
                        print('Material not found.')

                    w = mat['Wavelength, µm']
                    n_list = mat['n']
                    k_list = mat['k']

                    n = np.interp(wavelength, w, n_list) # interpolate the refractive index value
                    k = np.interp(wavelength, w, k_list) # interpolate the k value

                return n + k*1j

            # define the S object
            S = S4.New(Lattice=self.basis,
                       NumBasis=self.NumBasis)  # orthogonal basis, numbasis scales with memory O(N^2)

            # define materials
            for material in set(self.layer_material):
                if '|' in material:
                    doublet = material.split('|')
                    layer_medium = doublet[1] # the second material is the medium
                    layer_material = doublet[0] # the first material is the shape material
                    n1 = querry_n(layer_medium,self.wavelength)
                    n2 = querry_n(layer_material,self.wavelength)
                    S.SetMaterial(Name=layer_medium, Epsilon=n1**2)
                    S.SetMaterial(Name=layer_material, Epsilon=n2**2)
                else:
                    n = querry_n(material,self.wavelength)
                    # defines permittivity in terms of refractive index
                    eps = n**2
                    S.SetMaterial(Name=material, Epsilon=eps)
            S.SetMaterial(Name='Vacuum', Epsilon=1.0)

            # define layers
            S.AddLayer(Name='air_above', Thickness=self.buffer, \
                        Material='Vacuum')
            # iterate through all layers seperated by '/'
            for layer_index, _ in enumerate(self.layer_material):
                # define the variables used for the layer
                layer_material = self.layer_material[layer_index]
                layer_thickness = self.layer_thickness[layer_index]
                layer_pattern = self.layer_pattern[layer_index]
                layer_name = str(layer_index)

                if layer_pattern == None:
                    S.AddLayer(Name=layer_name, Thickness=layer_thickness,\
                                Material=layer_material)
                else:
                    # the default layer medium (the materials fills the space)
                    layer_medium = 'Vacuum'
                    if '|' in layer_material:
                        doublet = layer_material.split('|')
                        layer_medium = doublet[1] # the second material is the medium
                        layer_material = doublet[0] # the first material is the shape material
                    S.AddLayer(Name=layer_name, Thickness=layer_thickness, \
                                Material=layer_medium)

                    # iterate the patterns
                    for pattern in layer_pattern:
                        mat_and_pattern = pattern.split(':')
                        if len(mat_and_pattern) == 1:
                            pattern_material = layer_material
                        elif len(mat_and_pattern) == 2:
                            pattern_material = mat_and_pattern[0]
                            n = querry_n(pattern_material, self.wavelength)
                            S.SetMaterial(Name=pattern_material, Epsilon=n**2)
                            pattern = mat_and_pattern[1]
                        else:
                            raise Exception('Too many ":" in layer {}!'.format(layer_index))
                        shape = pattern[0]
                        coor = eval(pattern[1:])
                        if shape == 'C':
                            # create circle features
                            if type(coor)==float or type(coor)==int: coor = (0, 0, coor)
                            if coor[2] != 0:
                                S.SetRegionCircle(
                                    Layer = layer_name,
                                    Material = pattern_material,
                                    Center = (coor[0],coor[1]),
                                    Radius = coor[2]
                                )
                        elif shape == 'E':
                        # create ellipse
                            if (coor[3][0] != 0) and (coor[3][1] != 0):
                                S.SetRegionEllipse(
                                    Layer = layer_name,
                                    Material = pattern_material,
                                    Center = (coor[0],coor[1]),
                                    Angle = coor[2],
                                    Halfwidths = coor[3],
                                    )
                        elif shape == 'R':
                        # create rectangle
                            if (coor[3][0] != 0) and (coor[3][1] != 0):
                                S.SetRegionRectangle(
                                    Layer = layer_name,
                                    Material = pattern_material,
                                    Center = (coor[0],coor[1]),
                                    Angle = coor[2],
                                    Halfwidths = coor[3],
                                    )
                        elif shape == 'S':
                        # create square features
                            # if there is only 1 argument
                            if type(coor)==float or type(coor)==int: coor = (0, 0, coor)
                            if coor[2] != 0:
                                S.SetRegionRectangle(
                                    Layer = layer_name,
                                    Material = pattern_material,
                                    Center = (coor[0],coor[1]),
                                    Angle = 0,
                                    Halfwidths = (coor[2], coor[2])
                                )
                        elif shape == 'P':
                        # create a polygon
                            S.SetRegionPolygon(
                                    Layer = layer_name,
                                    Material =pattern_material,
                                    Center = (0,0),
                                    Angle = 0,            # in degrees
                                    Vertices = tuple(tuple(float(x) for x in i) for i in coor)
                            )

            S.AddLayer(Name='below', Thickness=self.buffer, Material='Vacuum')


            # simulation settings
            S.SetExcitationPlanewave(IncidenceAngles=(0.0, 0.0), sAmplitude=0.0,
                                     pAmplitude=1.0, Order=0)

            S.SetFrequency(1/self.wavelength)

            # For higher accuracy
            S.SetOptions(SubpixelSmoothing=True)

            # e is array of dimension Nx by Ny, each element is a tuple of length 3

            if  not self.transmission:
                z_pos = self.buffer/(2.0)
            else:
                z_pos = self.buffer*1.5+sum(self.layer_thickness)

            e, h = S.GetFieldsOnGrid(z=z_pos, NumSamples=(self.Nxy, self.Nxy),
                                     Format='Array')
            e = np.array(e)
            if not self.transmission:
                e = e - np.exp(1j*2*np.pi/self.wavelength*self.buffer/2)

            if FIELD==None:
                e_field = np.mean(e[:,:,0])  # adding 1 removes incident wave
            else:
                (a,b,_) = np.shape(e)
                edge = (1-FIELD)/2.0
                e_field = e[int(a*edge):int(a*(1-edge)),\
                int(b*edge):int(b*(1-edge)),0]

            e_field = np.round(e_field, 3)

            return pd.Series(str(e_field.tolist()))
