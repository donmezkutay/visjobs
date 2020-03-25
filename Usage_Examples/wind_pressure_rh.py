#!/usr/bin/env python
# coding: utf-8

# In[11]:


#importing dependencies
from visjobs.datas import get_data
from visjobs.visualize import draw_map
import xarray as xr

#getting the data using pick_data function of visjobs.datas
#hour=06 means the 06Z run of the model 
#here latest=True means the latest output with 06Z run
#model is chosen GFS can be changed to NAM also
#if hourly=False the GFS model will be 3 hourly -->only valid for GFS not for NAM
data = get_data.pick_data( hour='06',latest=True,model='GFS', hourly=False)


#here using xarray dataset,  we are dedicating the interval of desired latitude and longitude
# [0:2:1,:,:] means --> ['time', 'lon','lat']
press = data['prmslmsl'][0:2:1,:,:].sel(lat = slice(30,65), lon=slice(0,48))  / 100
ugrd =  data['ugrd10m'][0:2:1,:,:].sel(lat = slice(30,65), lon=slice(0,48) ) * 1.94384449
vgrd =  data['vgrd10m'][0:2:1,:,:].sel(lat = slice(30,65), lon=slice(0,48) ) * 1.94384449
rh =  data['rhprs'][0:2:1,:,:].sel(lat = slice(30,65), lon=slice(0,48) , lev=700) 
time = len(data['time'][0:2:1])



# In[15]:


#choosing the desired plot size
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 21,24

#place='europe' indicates the basin that user want to show as a plot.
#places avaliable for plotting
#places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans','indianocean'])
#if breaking=True only a single map will be created even if a bunch of time is introduced 
#if title_on=False the title will be missed
#if the title_on=True, title will be plotted and one can change it posisition arguments using
#tl1,tl2,tl3 etc. parameters.
# here tl5 is used to change the position of owner_name
#owner_name plots the upper-left sign.
draw_map.wind_pressure_rh(time, press, rh, ugrd, vgrd, place='europe',
                          save_where='Pictures\wind_pressure_rh{}.png', breaking=True, title_on=True ,owner_name='Kutay DÖNMEZ',
                         tl5=[0.0047, 0.98100])


# In[ ]:




