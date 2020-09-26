#get dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from visjobs.datas import get_MODEL
from visjobs.visualize import easy_plot
import cartopy
from matplotlib.collections import LineCollection
import seaborn as sns
import matplotlib as mpl

#get atlantic best track data from NHC
df = pd.read_csv(r'\hurdat2-1851-2019-052520.txt', sep=',')

#wrap the data
hur_dict = wrap_tc_data(df)

#adjust the data so that any specific hurricane can be picked up easily
deadliest_tc = ['KATRINA2', 'SANDY', 'MICHAEL2', 'HARVEY5', 'IRMA1', 'MARIA2']
all_matrises = {}
for tc in deadliest_tc:
    data_matris = sep_tc_data(hur_dict[tc], stack=False)
    tc_matris = adjust_data_spaces(data_matris)
    adjusted_matris = coords_str_to_float(tc_matris)
    all_matrises[tc] = adjusted_matris
    

#make the track map
m = easy_plot.painter()
ax = m.paint_ax(1,1,1, check_proj=True)
m.paint_borders(ax=ax, res='10m', zorder=4.5, linewidths=2.3, edgecolor='darkblue' )
oceans = ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'), facecolor = 'lightcyan')
m.paint_states(ax=ax, res='10m', zorder=4, linewidths=0.2, edgecolor='darkblue' )
land = ax.add_feature(cartopy.feature.LAND.with_scale('10m'), facecolor = 'bisque')
lake = ax.add_feature(cartopy.feature.LAKES.with_scale('10m'), facecolor = 'lightcyan', linewidths=1.2)
m.paint_coastline(ax=ax, res='10m', zorder=3, linewidths=1.5, edgecolor='darkblue')
m.paint_extent(ax=ax, lon_lat=[258,340,10,50])
m.set_lonlat(ax=ax, sizing=18)
m.set_size(ax=ax, a=21, b=19)

colormap = mpl.cm.Dark2.colors
m_styles = ['8','.','o','^','*','P','s']
TC_NAMES = ['KATRINA', 'SANDY', 'MICHAEL', 'HARVEY', 'IRMA', 'MARIA']


color_i = 0
for i in deadliest_tc:
    ax.plot(360-all_matrises[i][5], all_matrises[i][4], color=colormap[color_i], marker=m_styles[color_i] 
            ,transform=cartopy.crs.PlateCarree(), zorder=15, linewidth=2, label=TC_NAMES[color_i])
    
    
    
    color_i += 1

plt.legend( loc=1, borderaxespad=0.,ncol=3, prop={'size': 30});
title1 = m.set_title(title="USA Most Known Hurricanes In 2000's",ax=ax, fontsize=30, up=1.016, 
                     weight='heavy',style='italic',transform=ax.transAxes)

title2 = m.set_title(title='Kutay DÖNMEZ', color='k', right=0.00690, up=0.9652000, ax=ax, size=25, zorder=17,style='italic',transform=ax.transAxes,

                     bbox=dict(boxstyle="square",alpha=0.7,
                               ec='black',
                               fc='white',
                               ))

plt.savefig(r'\hurricanes{}.png'.format(i), bbox_inches='tight')

