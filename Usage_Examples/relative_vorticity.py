#!/usr/bin/env python
# coding: utf-8


get_ipython().system('git clone https://github.com/tomerburg/metlib.git')


#get dependencies
from visjobs.datas import get_MODEL
from visjobs.visualize import easy_plot
from metlib.diagnostics import met_functions
import xarray as xr
import matplotlib.pyplot as plt


#getting data and desired variables and desired area
data = get_data.pick_data(latest=True, hour='12', model='GFS', )
time, dt_dict = get_data.pick_area(data, total_process=32, interval=1, pr_height=['500'], list_of_vars=['ugrdprs', 'vgrdprs', 'hgtprs','prmslmsl'],
                                   list_of_areas=['europe'], )
#set data
uw = dt_dict['europe']['ugrdprs']
vw = dt_dict['europe']['vgrdprs']
hgt = dt_dict['europe']['hgtprs']
prs = dt_dict['europe']['prmslmsl'] / 100


#set lat lon
lat = uw.lat[:].values
lon = uw.lon[:].values


#computing all time steps of the relative vorticity 
rel_dict = {}
for i in range(len(uw['time'])):
    rel_vort= met_functions.relvort(uw[i,:,:], vw[i,:,:], lat, lon) * (10**5)
    
    rel_dict[i] = rel_vort 


#setting background style
plt.style.use('dark_background')
m = easy_plot.painter()

for i in range(len(uw['time'])):
    #paint features
    ax = m.paint_ax(1,1,1, check_proj=True)
    m.paint_borders(ax=ax, res='50m', zorder=4 )
    m.paint_land(ax=ax, res='50m', zorder=1)
    m.paint_coastline(ax=ax, res='50m', zorder=3, linewidths=1.1)
    m.paint_extent(ax=ax, lon_lat=[0,48,30,55])
    m.set_lonlat(ax=ax, sizing=18)
    m.set_size(ax=ax, a=21, b=19)

    #set interval
    rel_int = m.set_arange(-50, 51, 2, method='arange')
    hgt_int = m.set_arange(4680, 6121,20, method='arange')
    prs_int = m.set_arange(930, 1060, 4, method='arange')
    
    #make the MSLP contour
    mesh_prs = m.plot_contour(lon, lat, prs[i,:,:], prs_int, colors='purple', ax=ax,  linewidths=1.5, transform='PlateCarree', zorder=6)
    m.plot_clabel(mesh_prs, fontsize=20, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , ax=ax, zorder=5)

    #make the height contour
    mesh_hgt = m.plot_contour(lon, lat, hgt[i,:,:], hgt_int, colors='k', ax=ax,  linewidths=1.5, transform='PlateCarree', zorder=6)
    m.plot_clabel(mesh_hgt, fontsize=20, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , ax=ax, zorder=5)

    #make the relative vort. contourf
    mesh_2 = m.plot_contourf(lon, lat, rel_dict[i], rel_int, transform='PlateCarree', cmap='RdBu_r',  ax=ax, zorder=2 )
    cb = m.plot_colorbar(mappable=mesh_2, location='right', size='3%', pad='2%', ax=ax, sizing=17 )
    
    #set valid and init of the model
    valid = uw['time'][i].values 
    valid = str(valid)[0:13]
    init = str(uw['time'].attrs['grads_min'])
    
    #set titles
    title1 = m.set_title(title='RELATIVE VORTICITY(1e-5/s) | 500hPa HEIGHTS(m)',ax=ax, fontsize=30, up=1.016, 
                     weight='heavy',style='italic',transform=ax.transAxes)
    title2 = m.set_title(title='Init: {}'.format(init),right=0, up=-0.0920,ax=ax, fontsize=21,
                         style='italic', transform=ax.transAxes)
    title3 = m.set_title(title='Data: Global Forecast System 0.25°'.format(init),right=0, up=-0.0720,ax=ax, fontsize=21,
                         style='italic', transform=ax.transAxes)
    title4 = m.set_title(title='Codes: github.com/donmezk'.format(init),right=0, up=-0.1120,ax=ax, fontsize=21,
                         style='italic', weight='heavy', transform=ax.transAxes)
    title5 = m.set_title(title='Valid: {}'.format(valid), right=0.650, up=-0.0920, ax=ax, fontsize=30,
                         weight='heavy',style='italic', color='red', transform=ax.transAxes,
                         bbox=dict(boxstyle="square",alpha=0.7,
                               ec='red',
                               fc='white',
                               ))
    title6 = m.set_title(title='Kutay DÖNMEZ', color='k', right=0.00690, up=0.9652000, ax=ax, size=25, zorder=17,style='italic',transform=ax.transAxes,

                     bbox=dict(boxstyle="square",alpha=0.7,
                               ec='black',
                               fc='white',
                               ))
    
    #save figure
    plt.savefig('picturing\map{}'.format(i), bbox_inches='tight', edgecolor='w')
    
