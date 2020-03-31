# visjobs

Visjobs offers plotting effective variables in effective way using atmospheric models.

## Installation

- git clone https://github.com/donmezk/visjobs
- Clone in the same directory code is written.

### Some example about how to use Visjobs

- WE WILL BE PLOTTING THE 500MB GEOPOTENTIAL HEIGHT | MEAN SEA LEVEL PRESSURE FOR NORTH AMERICA
- importing dependencies.
```python

from visjobs.datas import get_data
from visjobs.visualize import draw_map
import xarray as xr
import numpy as np

```
------------


+ Getting the data using pick_data function.
+ Function pick_data():
    * hour=06      --> means the 06Z run of the model 
    * latest=True  --> means the latest output with 06Z run
    * model='GFS'  --> means GFS data is choosen ['NAM' is also available]
    * hourly=False --> means GFS 3 hourly data is asked [not valid for NAM]

```python

data = get_data.pick_data(hour='06',latest=True,model='GFS',
			  hourly=False)
```
+ Note that data taken is xarray DataArray.

------------


+ In below using xarray DataArray,  we are deciding the interval of desired latitude and longitude.
+ Returns a dictionary.
+ Function pick_area():
    * data          --> Xarray data must be given
    * total_process --> means until which time step the data is asked
    * interval      --> means until the asked time step, with what interval time step will go
    * init_time     --> means the initial time step of the data
    * list_of_vars  --> the desired variables in list [str]
    * list_of_areas --> the desired areas in list [str]
    * pr_height     --> the desired pressure heights in list [int]
    
```python

time, area_dict = get_data.pick_area(data, total_process=2, interval=1, init_time=0, 
				     list_of_vars=['prmslmsl','hgtprs'],pr_height=['500'],
                          	     list_of_areas=['northamerica','europe'])
```

+ Let's say I want to plot 500mb heights and mslp for Australia.
+ In the upper part I got the relevant data using pick_area function.
+ Now assign each single data from the whole dictionary.
```
press = np.divide(area_dict['northamerica'][0], 100)
heightprs = area_dict['northamerica'][1]
```

- Choosing the desired plot size.

```python
from pylab import rcParams
rcParams['figure.figsize'] = 21, 24
```

+ In below using height_pressure function we will plot 500mb Height-Pressure graphic
+ Function height_pressure():
    * time       --> the loop initiated from the init_time indicated above function until the 'time'
    * press      --> xarray input for pressure
    * heightprs  --> xarray input for height
    * pr_height  --> the desired pressure height
    * place      --> the area which the user wants to plot
    * save_where --> where to save the figure
    * breaking   --> if True, the function will stop after one loop
    * title_on   --> if True, the title must be introduced, default is False
    * ----------------------------------------------------------------------
        * if only the title_on = True, apply inputs below
    * owner_name = the box in the upper left corner of the plot
    * plot_main_tite 	       --> main title that is going to be plotted in string
    * tl1, tl2, tl3, tll4, tl5 --> set the title's placement [a,b] (int list)

```python
draw_map.height_pressure(time, press, heightprs ,pr_height='500', place='northamerica',
                         save_where=r'height_prs{}.png',
			 breaking=True, title_on=True ,owner_name='Kutay DÖNMEZ',
			 plot_main_title=r'GFS 500mb Geopotential Height(m) | Presssure(mb)',
                         tl5=[0.0047, 0.97100], tl1=[0,1.032])
```
plot result:
https://pasteboard.co/J1HhgsF.png
![]('https://pasteboard.co/J1HhgsF.png')
