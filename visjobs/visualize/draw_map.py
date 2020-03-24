#!/usr/bin/env python
# coding: utf-8
import warnings
warnings.filterwarnings("ignore")
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import cartopy
import numpy as np
import matplotlib as mpl
import scipy.ndimage as ndimage
import matplotlib.colors as mcolors
from netCDF4 import num2date
from matplotlib.animation import ArtistAnimation
import numpy as np
import matplotlib.animation as animation

def arrangements_of_extras(title1=[], title2=[], title3=[], title4=[], title5=[]):
    return title1, title2, title3, title4, title5

def wind_pressure_rh(time_on, pressure, hum, u, v, lon_iso, lat_iso, extent=[], hourly=3, 
                      save_where='wind_pressure_rh{}.png'
                     , breaking=True, tl1=[0,1.02], tl2=[0,1.0050], 
                     tl3=[0.5,1.0050], tl4=[0.81000,1.0050], tl5=[0.0047, 0.98422]):
    
    #define starting time
    start_time_all = datetime.now()

    #define our loop ingredients
    toplam=0
    say=0
    for t in range(time_on):
        #define variables
        press = pressure.sel(time=pressure['time'][t] ) 
        rh = hum.sel(time=hum['time'][t] ) 
        uwind = u.sel(time=u['time'][t] ) 
        vwind = v.sel(time=v['time'][t] ) 
        ww = np.sqrt(uwind**2+vwind**2)


        #define valid time using the time dim of the var
        valid = pressure['time'][t].values # buradaki time'da hata vericek sonra
        valid = str(valid)[0:13]
    
        #define our axis
        my_dpi = 96
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection=cartopy.crs.Mercator())
        
        #define our features
        ax.add_feature(cartopy.feature.BORDERS.with_scale('10m') , linewidths = 0.4, zorder=13)
        ax.add_feature(cartopy.feature.COASTLINE.with_scale('10m') , linewidths=0.6, zorder=14)
        ax.add_feature(cartopy.feature.LAND.with_scale('10m') ,facecolor='lightgrey')
        
        #defining extent area
        ax.set_extent(extent)
        
        #define a colormap
        c1 = plt.cm.cool(np.linspace(0., 1, 256))
        c3 = plt.cm.gist_gray(np.linspace(0., 1, 256))
        c2 = plt.cm.autumn_r(np.linspace(0., 1, 256))
        c0 = plt.cm.pink_r(np.linspace(0., 0.5, 256))
        cols = np.vstack((c0,c1,c2,c3))
        mymap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', cols)

        #define our arranges of variables will be ploted
        tm_pressure = np.arange(920,1051,2)
        tm_rh =  np.arange(80,101,5)
        tm_wind = np.arange(0, 89, 2)
        
        #gridline
        ax.gridlines()
       
        #contourplot for MSLP
        mesh_press=ax.contour(lon_iso, lat_iso, press, tm_pressure, transform = cartopy.crs.PlateCarree(), colors='k' ,
                   linestyles='solid', linewidths=0.9)

        ax.clabel(mesh_press, fontsize=18, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , )
        
        #contourplot for RH
        mesh_rh=ax.contour(lon_iso, lat_iso, rh, tm_rh, cmap='Greens', transform = cartopy.crs.PlateCarree() ,
                   linestyles='solid' , linewidths=0.9)

        ax.clabel(mesh_rh, fontsize=18, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , )
        
        #meshplot for wind speed
        mesh_ww=ax.contourf(lon_iso, lat_iso, ww ,tm_wind, cmap=mymap, extend='both', alpha=0.6,
                                transform = cartopy.crs.PlateCarree())
        

        wind_slicelat = slice(5, -5, 7)
        wind_slicelon = slice(5, -5, 3)
        
        
        title1 = ax.text(tl1[0],tl1[1],'GFS MSLP(hPa)|10m Wind(knots)|700hPa RH(%80 to %100 Green Contours)',transform=ax.transAxes,fontsize=23, weight='bold',style='italic')
        title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(pressure['time'][0].values)[0:13]),transform=ax.transAxes,fontsize=17,style='italic')
        title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=18,style='italic')
        title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=18,weight='heavy',style='italic')
        title5 = ax.text(tl5[0],tl5[1], "Kutay & Berkay DONMEZ",transform=ax.transAxes, size=18,zorder=17,style='italic',

             bbox=dict(boxstyle="square",alpha=0.7,
                       ec='black',
                       fc='white',
                       ))
        
        #check if the data is hourly or 3 hourly or 12 hourly
        if hourly == 1:
            toplam += 1
        elif hourly == 3:
            toplam += 3
        elif hourly == 12:
            toplam += 12

        
        #define our colorbar
        #cb = plt.colorbar(mesh_ww, fraction, pad, orientation='horizontal' )
        #cb.ax.tick_params(labelsize=17)
        
        #save the fig
        plt.savefig(save_where.format(t) , bbox_inches='tight')
        
        #inform user map count going
        say+=1
        print('wind_pressure_rh | {}.map | Done--{}'.format(say,datetime.now().time()))



        if breaking == True:
            break




    end_time_all = datetime.now()
    print('wind_pressure_rh | TOTAL JOB DONE | Duration: {}'.format(end_time_all - start_time_all))

    
def temp_rh_cross_aegean(time_on, temp, hum, height_iso, lat_iso, hourly=3, 
                      save_where='temp_rh_cross{}.png'
                     , breaking=True, tl1=[0,1.04], tl2=[0,1.0080], 
                     tl3=[0.5,1.0080], tl4=[0.77000,1.0080], tl5=[0.0050, 0.9700]):

    #define starting time
    start_time_all = datetime.now()
    
    
    #define our loop parameters
    toplam=0
    say=0
    
    for t in range(time_on):
        #define our variables
        temperature = temp.sel(time=temp['time'][t] ) 
        rhum = hum.sel(time=hum['time'][t])
        
        #set validity
        valid = temp['time'][t].values
        valid = str(valid)[0:13]
        
        #define our axis
        my_dpi = 96
        fig = plt.figure(figsize=(14,10))
        ax = fig.add_subplot(1,1,1)
        
        #define our colorbar
        c1 = plt.cm.winter(np.linspace(0., 1, 256))
        c3 = plt.cm.PiYG(np.linspace(0.75, 1, 256))
        c2 = plt.cm.autumn_r(np.linspace(0., 1, 256))
        c0 = plt.cm.PuRd(np.linspace(0., 1, 256))
        cols = np.vstack((c0,c1,c2,c3))
        mymap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', cols)

        #define our arrangement for plotting our variables
        tm = np.arange(-40 , 41 , 2)
        r = np.arange(0 , 101 , 5)

        #contour our temperature
        mesh_temp=ax.contour(lat_iso,height_iso, temperature ,tm, cmap=mymap ,
                    linestyles='solid' , linewidths=0.8)
        ax.clabel(mesh_temp, fontsize=16, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True )

        #contour our humidity
        mesh_rh=ax.contour(lat_iso,height_iso, rhum ,r, colors='green' ,
                    linestyles='solid' , linewidths=0.4)
        ax.clabel(mesh_rh, fontsize=12, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True  )
        
        #mesh our humidity
        mesh_hum=ax.contourf(lat_iso,height_iso,rhum ,r,cmap='Greens',extend='both', )
                        
        #label and set size of our axeses
        plt.ylabel('Pressure(hPa)', fontsize=16,weight='heavy',style='italic')
        plt.xlabel('Latitude(°N)', fontsize=16,weight='heavy',style='italic')
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', labelsize=14)
        
        #invert y axis with pressure decreasing upward
        ax.invert_yaxis()
        
        #arrange the titles of map
        title = ax.text(tl1[0],tl1[1],'GFS 36°N-40°N | mean(26.5°E-27.5°E) Aegean Reg.| Height-Temp(°C)-RH(%)',color='navy',transform=ax.transAxes,fontsize=17, weight='bold',style='italic')
        title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(temp['time'][0].values)[0:13]),transform=ax.transAxes,fontsize=14,style='italic')
        title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=15,style='italic')
        title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=15,weight='heavy',style='italic')
        title5 = ax.text(tl5[0],tl5[1], "Kutay & Berkay DONMEZ",transform=ax.transAxes, size=15,zorder=17,style='italic',


             bbox=dict(boxstyle="square",alpha=0.7,
                       ec='black',
                       fc='white',
                       ))
                        
        #set with which interval the hour will change 
        if hourly == 1:
            toplam += 1
        elif hourly == 3:
            toplam += 3
        elif hourly == 12:
            toplam += 12

        #arrange our second axisis placement showing where the cross section is implied
        
        left, width = 0.07, 0.65
        bottom = 0.6
        height = 0.280
        left_h = left+width+0.0305
        rect_box = [left_h, bottom, 0.21, height]
        
        #set second axes
        ax2 = plt.axes(rect_box,projection=cartopy.crs.Mercator())
                        
        #provide sets to not seen
        ax2.get_yaxis().set_ticks([])
        ax2.get_xaxis().set_ticks([])

        #define map using cartopy for second axes 
        ax2.add_feature(cartopy.feature.BORDERS.with_scale('10m') , linewidths = 0.5)
        ax2.add_feature(cartopy.feature.COASTLINE.with_scale('10m') , linewidths=0.9)
        ax2.add_feature(cartopy.feature.LAND.with_scale('10m') ,zorder=0,facecolor='brown')
        ax2.set_extent([25,29,35,42])
        
        #show the cross section area in the second axis map
        ax2.plot([26.5,26.5],[36,40], c='k',transform = cartopy.crs.PlateCarree())
        ax2.plot([27.5,27.5],[36,40], c='k',transform = cartopy.crs.PlateCarree())
        ax2.plot([26.5,27.5],[36,36], c='k',transform = cartopy.crs.PlateCarree())
        ax2.plot([26.5,27.5],[40,40], c='k',transform = cartopy.crs.PlateCarree())
        
        ax2.scatter([26.5,26.5],[36,40], c='k',transform = cartopy.crs.PlateCarree())
        ax2.scatter([27.5,27.5],[36,40], c='k',transform = cartopy.crs.PlateCarree())
        ax2.scatter([26.5,27.5],[36,36], c='k',transform = cartopy.crs.PlateCarree())
        ax2.scatter([26.5,27.5],[40,40], c='k',transform = cartopy.crs.PlateCarree())


        #save our figure
        plt.savefig(save_where.format(t) , bbox_inches='tight')
        
        #infrom user map count going on
        say+=1
        print('Temp_rh_cross | {}.map | Done--{}'.format(say,datetime.now().time()))

        if breaking == True:
            break







    end_time_all = datetime.now()
    print('TEMP_PRESS_TURKEY | TOTAL JOB DONE | Duration: {}'.format(end_time_all - start_time_all))

