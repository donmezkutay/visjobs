# visjobs

Visjobs offers plotting effective variables in effective way using atmospheric models.

## 1.Installation

#### 1.1. Dependencies (Suggestion: Install these packages below using Anaconda, installing them using pip is not efficient.)
- xarray
- pydap
- twine
- siphon
- pandas
- numpy
- matplotlib
- cartopy
- datetime

#### 1.2. Pypi Installation
- pip install visjobs==0.0.15

#### 1.3. Github Clone
- git clone https://github.com/donmezkutay/visjobs

## 2. Usage
Once you installed visjobs, you can easily get the latest atmospheric model data including GFS, GEFS, and NAM.
You can also get the GHCN(Global Historical Climatology Network) observation data for each station.

#### 2.1. Getting The Xarray Dataset
##### GFS (0.25 Degree)
Get the latest 12 UTC GFS (0.25 Degree) 3 hourly Data.
This wil return Xarray Dataset.
``` python
from visjobs.datas import get_MODEL
data = get_MODEL.pick_data(hour='12',latest=True,
                          model='GFS', hourly=False,
                          resolution = 0.25)
```

##### GFS (0.50 Degree)
Get yesterday's 00 UTC GFS (0.25 Degree) 1 hourly Data.
Change year/month/day with your yesterday (Available until previous week).
``` python
data = get_MODEL.pick_data(year='2020', month='09',day='03',
                          hour='00', latest=False,
                          model='GFS', hourly=True)
```

##### GEFS (0.50 Degree)
Get 3 days before's 06 UTC GEFS (0.50 Degree) 3 hourly Data.
Change year/month/day with your 3 days before (Available until previous week).
``` python
data = get_MODEL.pick_data(year='2020', month='09',day='01',
                          hour='06', latest=False,
                          model='GEFS', hourly=False)
``` 

##### NAM (12 km / CONUS)
Get the latest 18 UTC NAM (12 km) 3 hourly Data.
``` python
data = get_MODEL.pick_data(hour='18', latest=True,
                          model='NAM', hourly=False)
``` 

##### HRRR (0.029 Degree / CONUS)
Get the latest 14 UTC HRRR (0.029 Degree) 1 hourly Data.
``` python
data = get_MODEL.pick_data(hour='14', latest=True,
                          model='HRRR', hourly=True)
``` 

##### NBM_1HR (National Blend of Models / CONUS)
Get the latest 21 UTC NBM 1 hourly Data.
``` python
data = get_MODEL.pick_data(hour='21', latest=True,
                          model='NBM_1HR', hourly=True)
``` 

##### NBM_3HR (National Blend of Models / CONUS)
Get the latest 13 UTC NBM 3 hourly Data.
``` python
data = get_MODEL.pick_data(hour='13', latest=True,
                          model='NBM_3HR',)
``` 

##### NBM_6HR (National Blend of Models / CONUS)
Get the latest 16 UTC NBM 6 hourly Data.
``` python
data = get_MODEL.pick_data(hour='06', latest=True,
                          model='NBM_6HR',)
``` 

##### Using DASK Chunks with Xarray (DASK library required to be installed beforehand)
You can also get the model data with dask chunks such as:
``` python
data = get_MODEL.pick_data(hour='18', latest=True,
                          model='GFS', hourly=False,
                          chunks = {'time': -1,
                                    'lon' : 80,
                                    'lat' : 80,
                                    'lev' : -1 })
``` 

##### GHCN Observation Data
Get GHCN Climatology data for station ID:'TUM00017064' (Istanbul Bolge-Kartal).
This will return Pandas DataFrame.
``` python
from visjobs.datas import get_GHCN as ghc
dt = ghc.get_data_with_station('TUM00017064')
``` 

For users want to easily access to Turkey's station IDs, the code below will return avaliable IDs for Turkey
``` python
#ghc.get_turkey_ID()
#this code is currently unavailable --> v0.0.15
``` 

##### ERA-5 (0.25 Degree)
Let's say we want to get the ERA-5 0.25 degree hourly pressure and single data for date 2005-08-29.
``` python
from visjobs.datas import get_ERA5
username = 'rda ucar login username'
password = 'rda ucar password'
u, v, z, q, w, vo, t = get_ERA5.get_pressure_variables(username, password, '20050829', parse='all')
t2, msl, cape, u10, v10 = get_ERA5.get_single_variables(username, password, '20050829', 'august', parse='all')
``` 

Also by changing "parse" argument you can narrow down the area for the dataset only to Turkey. Such as:
``` python
username = 'rda ucar login username'
password = 'rda ucar password'
u, v, z, q, w, vo, t = get_ERA5.get_pressure_variables(username, password, '20050829', parse='turkey')
``` 

#### 2.2. Arranging The Xarray Dataset
Visjobs has a function that will return desired model variables for some of the pre-defined specific world regions including Europe, North America, Australia etc.  

Let's say we want to pull MSLP and 500 mb Geopotential Height variables from our previously defined Xarray dataset <data> for North America and Europe.
```python

area_dict = get_MODEL.pick_area(
                            data, init_time=0, 
                            total_process=2, interval=1, 
		            list_of_vars=['prmslmsl','hgtprs'],
		            pr_height=['500'],
                            list_of_areas=['northamerica','europe'])
```
here;
* data: Xarray dataset must be given
* total_process: means until which time step the data is asked [int]
* interval: means until the asked time step, with which interval time step will go [int]
* init_time: means the initial time step of the data [int]
* list_of_vars: the desired variables in list [str]
* list_of_areas: the desired areas in list [str]
* pr_height: the desired pressure heights in list [str]

With one code step forward you can seperate the data you choose into appropriate pieces:
```python
mslp_NA = np.divide(area_dict['northamerica']['prmslmsl'], 100)
mslp_E  = np.divide(area_dict['europe']['prmslmsl'], 100)

height_NA = area_dict['northamerica']['hgtprs']
height_E  = area_dict['europe']['hgtprs']
```

#### 2.3. Visualizing the Xarray Dataset
Until now, we show some of the capabilities of the visjobs. Yet, Of course the visualization of the data is maybe the most important part of the analysis.

So, now on, we will be writing a code that uses the abilities of the visjobs to get the dataset and arrange it. And then we will be visualizing it using visjobs easy_plot function.

Here we will be getting the latest 06 UTC GFS (0.25 Degree) data, picking the MSLP and 10m U,V Wind variables in the dataset and plotting them for Gulf Of Mexico.
```python
from visjobs.datas import get_MODEL
from visjobs.visualize import easy_plot
import xarray as xr
import matplotlib.pyplot as plt
import proplot as plot
import numpy as np
import cartopy

data = get_MODEL.pick_data(latest=True, hour='06', model='GFS')

area_dict = get_MODEL.pick_area(
                            data, init_time=0, 
                            total_process=3, interval=1, 
			    list_of_areas=['northamerica'],
			    list_of_vars=['prmslmsl','ugrd10m',
				          'vgrd10m'],)

#Seperate data
prs = np.divide(area_dict['northamerica']['prmslmsl'], 100) #convert to hPa
u10 = np.multiply(area_dict['northamerica']['ugrd10m'], 1.94384449) #convert to knot
v10 = np.multiply(area_dict['northamerica']['vgrd10m'], 1.94384449) #convert to knot

#calculate wind speed from u and v wind
ww = np.sqrt((u10**2) + (v10**2))

#indicate latitude and longitude
lon = u10['lon']
lat = u10['lat']

#get cmap
cmap = 'gnuplot2_r'

#start easy_job instance
m = easy_plot.painter()

#paint features
ax = m.paint_ax(1,1,1, check_proj=True)
m.paint_borders(ax=ax, res='10m', zorder=4, 
                linewidths=1.5, edgecolor='red' )

m.paint_states(ax=ax, res='10m', zorder=4, 
               linewidths=1.5, edgecolor='red' )

m.paint_lakes(ax=ax, res='10m', zorder=4, 
              linewidths=1.5, edgecolor='red' )

m.paint_land(ax=ax, res='10m', zorder=1)
m.paint_coastline(ax=ax, res='10m', zorder=3, 
                  linewidths=1.5, edgecolor='red')

m.paint_extent(ax=ax, lon_lat=[260,292,20,40])
m.set_lonlat(ax=ax, sizing=18)
m.set_size(ax=ax, a=21, b=19)

#set interval
wind_int = m.set_arange(0, 90, 2, method='arange')
prs_int  = m.set_arange(930, 1060, 2, method='arange')
    

#plot the pressure contour
mesh_hgt = m.plot_contour(lon, lat, prs[0], 
                          prs_int, colors='k', 
                          ax=ax,  linewidths=2, 
                          transform='PlateCarree', 
                          zorder=6, linestyles='solid')

m.plot_clabel(mesh_hgt, fontsize=30, 
              inline=1, inline_spacing=7,
              fmt='%i', rightside_up=True,
              use_clabeltext=True , 
              ax=ax, zorder=5)
              
#plot the wind contourf
mesh_2 = m.plot_contourf(lon, lat, ww[0], 
                         wind_int, transform='PlateCarree',
                         cmap=cmap,  ax=ax, zorder=2 )

#plot the colorbar
cb = m.plot_colorbar(mappable=mesh_2, location='right',
                     size='3%', pad='2%', ax=ax, sizing=17 )
    
#set validation times
valid = u10['time'][0].values 
valid = str(valid)[0:13]
init  = str(u10['time'].attrs['grads_min'])

#set titles
title1 = m.set_title(title='10m WIND SPEED (kt) | MSLP (hPa)',
                     ax=ax, fontsize=30, up=1.016, 
                     weight='heavy',style='italic',
                     transform=ax.transAxes)

title2 = m.set_title(title='Init: {}'.format(init),
                     right=0, up=-0.1020,ax=ax, 
                     fontsize=21, style='italic', 
                     transform=ax.transAxes)

title3 = m.set_title(title='Data: GFS 0.25°'.format(init),
                     right=0, up=-0.0720,ax=ax,
                     fontsize=21, style='italic', 
                     transform=ax.transAxes)

title4 = m.set_title(title='Codes: github.com/donmezkutay',
                     right=0, up=-0.1320,ax=ax, 
                     fontsize=21, style='italic', 
                     weight='heavy', transform=ax.transAxes)

title5 = m.set_title(title='Valid: {}'.format(valid),
                     right=0.650, up=-0.0920, ax=ax,
                     fontsize=30, weight='heavy',
                     style='italic', color='red', 
                     transform=ax.transAxes,
                     bbox=dict(boxstyle="square",alpha=0.7,
                               ec='red',
                               fc='white',
                               ))

title6 = m.set_title(title='visjobs', color='k', right=0.00690,
                     up=0.9652000, ax=ax, size=25, zorder=17,
                     style='italic',transform=ax.transAxes,
                     bbox=dict(boxstyle="square",alpha=0.7,
                               ec='black',
                               fc='white',
                               ))
```
plot result:
https://pasteboard.co/JpxKXQC.png

