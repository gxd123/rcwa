# rcwa
A S4 wrapper to make RCWA simulations with ease. 


---
## Installation 

`pip install https://github.com/Luochenghuang/rcwa/raw/master/dist/rcwa-0.0.2.tar.gz`



---
## Dependencies
S4



---
## Usage
```python
# make input array of CSCS strings
cscs_array = []
periodicity = 0.45

for wavelength in [0.7, 0.54]:
    for r in r_list:
        inpt = 'r-{}-({},0.),(0.,{})/TiO2=0.5:C(0,0,{})/SiO2=0.4/Ag=1.1'\
          .format(wavelength,periodicity,periodicity,r)
        cscs_array.append(inpt)

# start simulation
new = RCWA(cscs_array, 19, field=1) # uses 19 cores and all the electric field of 1 unit cell
df = new.simulate()

# save simulation data
df.to_csv('test.csv', index=False)
```



---
## CSCS
<img src="https://github.com/Luochenghuang/rcwa/raw/master/doc/CSCS%20Helper.jpg" alt="some text"  width="1050" height="784">


