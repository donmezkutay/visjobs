# -*- coding: utf-8 -*-
"""


@author: Kutay
"""

from visjobs.datas import get_data
from visjobs.visualize import draw_map
from visjobs.visualize import easy_plot

import numpy as np
import xarray as xr

data = get_data.pick_data(year='2020', month='03', day='29', hour='18', model='GFS', resolution=0.25)

time, dt_dict = get_data.pick_area(data, init_time=0 ,total_process=10, interval=1, 
                                       list_of_vars=['prmslmsl', 'tmp2m'],
                                       list_of_areas=['europe'],pr_height=[500])

pr = np.divide(dt_dict['europe'][0],100) #to hPa
temp = np.subtract(dt_dict['europe'][1],273.15) #DegreeC

lon = pr.lon[:].values
lat = pr.lat[:].values


#enter class and make axis
m = easy_plot.painter()
ax = m.paint_ax(1,1,1, check_proj=True, proj='Mercator')

#set features
m.paint_borders(ax=ax, zorder=13)
m.paint_coastline(ax=ax)
m.paint_land(ax=ax, zorder=0)
m.paint_states(ax=ax, zorder=14)
m.paint_extent(ax=ax, lon_lat = [0,48,30,60])
m.set_size(19,21,ax=ax)
m.set_gridlines(ax=ax)
m.set_lonlat(ax=ax)

#Define arrays will be used
int_pr = m.set_arange(920,1060,2, method='arange')
int_temp = m.set_arange(-40,40,2, method='arange')

#Make The plots
mesh = m.plot_contour(lon, lat, pr[0,:,:], int_pr, colors='k', linestyles='solid',ax=ax,  linewidths=0.9, transform='PlateCarree')
m.plot_clabel(mesh, fontsize=16, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , ax=ax)
mesh_2 = m.plot_contourf(lon, lat, temp[0,:,:], int_temp, transform='PlateCarree', cmap='gist_ncar', alpha=0.6, ax=ax )
cb = m.plot_colorbar(mappable=mesh_2, location='bottom', pad='3%', ax=ax)
m.set_title(title='GFS 2m Temperature | MSLP',ax=ax, fontsize=35)