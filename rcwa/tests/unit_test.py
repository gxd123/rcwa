import imp
rcwa = imp.load_source('*', '../rcwa.py') # for python 2.7
import os.path as op
import numpy as np
import pandas as pd
import numpy.testing as npt
import sys
import unittest

class TestSimpleShapes(unittest.TestCase):
    
    def test_combo_geometries(self):
        inputs = ['r-0.55-(0.5,0.),(0.,0.5)/TiO2=1:C(0,0,0.2)/SiO2=1/Ag=1.1']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum = np.abs(np.sum(eval(df['e_field'][0])))
        self.assertEqual(check_sum, 2470.1178851384807)
        
    def test_just_a_slab(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum = np.abs(np.sum(eval(df['e_field'][0])))
        self.assertEqual(check_sum, 2476.633736021537)
        
    def test_multiprocessing(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1', 't-0.55-(0.5,0.),(0.,0.5)/TiO2=2']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        check_sum2 = np.abs(np.sum(eval(df['e_field'][1])))
        self.assertEqual(check_sum1, 2476.633736021537)
        self.assertEqual(check_sum2, 2122.8122223126566)
        
    def test_circle(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1:C(0,0,0.22)', \
                  't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:C(0.1,0.1,0.1)', \
                  't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:C(0,0,0)',]
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        check_sum2 = np.abs(np.sum(eval(df['e_field'][1])))
        check_sum3 = np.abs(np.sum(eval(df['e_field'][2])))
        self.assertEqual(check_sum1, 2108.347107570525)
        self.assertEqual(check_sum2, 2622.9165329237985)
        self.assertEqual(check_sum3, 2703.9486235119193)
        
    def test_square(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1:S(0,0,0.22)', \
                  't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:S(0.1,0.1,0.1)', \
                  't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:S(0,0,0)',]
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        check_sum2 = np.abs(np.sum(eval(df['e_field'][1])))
        check_sum3 = np.abs(np.sum(eval(df['e_field'][2])))
        self.assertEqual(check_sum1, 2206.9687181906315)
        self.assertEqual(check_sum2, 2642.184679057844)
        self.assertEqual(check_sum3, 2703.9486235119193)
        
    def test_combo_only_index(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/[3.5, 0]=1:C(0,0,0.2)/[2, 0]=1']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum = np.abs(np.sum(eval(df['e_field'][0])))
        self.assertEqual(check_sum, 1548.0511113584073)
        
    def test_ellipse(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1:E(0,0,0, (0.22, 0.22))',\
                 't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:E(0,0,0, (0.2, 0.3))',\
                 't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:E(0,0,0, (0.1, 0.2))']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        check_sum2 = np.abs(np.sum(eval(df['e_field'][1])))
        check_sum3 = np.abs(np.sum(eval(df['e_field'][2])))
        self.assertEqual(check_sum1, 2108.347107570525)
        self.assertEqual(check_sum2, 909.407190919997)
        self.assertEqual(check_sum3, 1957.9150336099879)
        
    def test_rectangle(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1:R(0,0,0, (0.22, 0.22))',\
                 't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:R(0,0,0, (0.2, 0.3))',\
                 't-0.55-(0.5,0.),(0.,0.5)/TiO2=1:R(0,0,0, (0.1, 0.2))']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        check_sum2 = np.abs(np.sum(eval(df['e_field'][1])))
        check_sum3 = np.abs(np.sum(eval(df['e_field'][2])))
        self.assertEqual(check_sum1, 2206.9687181906315)
        self.assertEqual(check_sum2, 2615.3841447015006)
        self.assertEqual(check_sum3, 2655.7338944828416)
        
    def test_polygon(self):
        inputs = ['t-0.55-(0.5,0.),(0.,0.5)/TiO2=1:P((0,0),(0.2,0),(0.2,0.2))']
        S = rcwa.RCWA(inputs, 19, field=1)
        df = S.simulate()
        check_sum1 = np.abs(np.sum(eval(df['e_field'][0])))
        self.assertEqual(check_sum1, 1000.2224936532872)

