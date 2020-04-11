#!/usr/bin/env python
# coding: utf-8

#importing dependencies
from visjobs.datas import get_data
from visjobs.visualize import draw_map
import xarray as xr
import numpy as np

#getting the data using pick_data function of visjobs.datas
#hour=06 means the 06Z run of the model 
#here latest=True means the latest output with 06Z run
#model is chosen GFS can be changed to NAM also
#if hourly=False the GFS model will be 3 hourly -->only valid for GFS not for NAM
data = get_data.pick_data( hour='00',latest=True,model='GFS', hourly=False)



# here we are getting the desired variables with desired areas of interest,returned in dictionary
time, area_dict = get_data.pick_area(data, total_process=-1, interval=4,
                                     list_of_vars=['prmslmsl','ugrd10m','vgrd10m','rhprs'],pr_height=['700'],
                          list_of_areas=['europe'])

#let's say I want to plot wind, pressure and 700hPa RH for Australia
#so in the upper part I got the relevant data using pick_area function
#so let's wrap the data:
press = np.divide(area_dict['europe'][0], 100) #setting the unit
ugrd = np.multiply(area_dict['europe'][1], 1.94384449)
vgrd = np.multiply(area_dict['europe'][2], 1.94384449)
rh = area_dict['europe'][3]



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
                          save_where=r'C:\Users\Kutay\visjobs\picturing\wind_pressure_rh{}.png',
                          breaking=False, title_on=True ,owner_name='Kutay DÖNMEZ',
                          plot_main_title=r'GFS 10m Winds(knots) | MSLP(hPa) | 700hPa RH(%80 to %100)',
                         tl5=[0.0047, 0.98100])






