# rcwa
A S4 wrapper to make RCWA simulations with ease. 

## Installation 

`pip install https://github.com/Luochenghuang/rcwa/raw/master/dist/rcwa-0.2.0.tar.gz`

## Test

Go to the rcwa/tests/ folder and run
`python -m unittest -v unit_test`


## Dependencies
S4


## Usage
```python
# this is just a snippet of the example.py in the example folder. Does not actually run.
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


## CSCS
<img src="https://github.com/Luochenghuang/rcwa/raw/master/doc/CSCS%20Helper.jpg" alt="some text"  width="1050" height="784">

### Custom material
You can replace the material with [n, k] to manually input the refractive index.

### Change medium
By default, anytime you add a shape the material surrounds that shape is vacuum. 
If you desire to change that, simply use `{shape_material}|{medium}`.

For instance, `TiO2=1:C(0.2)` gives you a circle of radius 0.2 the medium is vacuum. 
If you wish to change from vacuum to SiO2, then use `TiO2|SiO2=1:C(0.2)`.

### Change material of the shape
By default, the shapes all have the same material defined at the start before the `=` sign. 
If you want to have a different material, do `{material}:C(0.1)`.
For instance, `TiO2=1:C(0.2)-Vacuum:C(0.1)` gives you a circular pillar with radius 0.2 that contains a vacuum core of radius 0.1.

### Circle
Add a circle by `C(x,y,radius)`.
Alternatively use `C(radius)` for shorthand which defaults x, y = 0, 0

### Square
Add a square by `S(x, y, halfwidth)`
Alternatively use `S(radius)` for shorthand which defaults x, y = 0, 0

### Rectangle
Add a rectangle by `R(x, y, angle, (x_halfwidth, y_halfwidth))` where angle is in degrees

### Ellipse
Add an ellipse by using `E(x, y, angle, (r1, r2))`, where x and y are the center coordinates, angle is the rotation, r1 and r2 are the conjugate diameters/2.

### Polygon
Add a polygon by using `P((x1, y1), (x2, y2), ... , (x1, y1))` where xn, yn, is a vertex pair.
