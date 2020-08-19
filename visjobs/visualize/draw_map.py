#!/usr/bin/env python
# coding: utf-8
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import cartopy
import matplotlib as mpl
import numpy as np

def arrangements_of_extras(title1=[], title2=[], title3=[], title4=[], title5=[]):
    return title1, title2, title3, title4, title5

def wind_pressure_rh(time_on, pressure, hum, u, v, place='europe',
                     hourly=3, 
                      save_where='wind_pressure_rh{}.png',title_on=False
                      ,owner_name='Kutay&Berkay DONMEZ',
     plot_main_title=''
                     , breaking=True, tl1=[0,1.02], tl2=[0,1.0050], 
                     tl3=[0.5,1.0050], tl4=[0.81000,1.0050], tl5=[0.0047, 0.98422]):
    """ Returns a pre-prepared windspeed-pressure-rh plot
        
    time_on=indicates the count of maps(hours) will be plotted
    extent:
        
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans'])
    
    If title_on=False the titles will not be seen, unless the title_on=True,
    Default is False.
    
    NOTE:Please Input Xarray DataArray
    """
    
    #warn user to only input xarray dataset as variables
    try:
        press = pressure.sel(time=pressure['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
        
    try:
        rh = hum.sel(time=hum['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
    
    try: 
        uwind = u.sel(time=u['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray') 
    
    try:vwind = v.sel(time=v['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
    
    #defining lon and lat
    lon_iso = pressure.lon[:].values
    lat_iso = pressure.lat[:].values
    
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans','indianocean','northatlantic'])
    
    #extents corresponding to the places defined
    extents = np.array([[0, 48, 30, 60],[218,318,-5,55],
                        [80,180,-40,0],[260,285,23,26],[275,300,17,33],[30, 130,-20,20],
                        [300, 359,43,64]])
        
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
        for i in range(len(places)):
            if place == places[i]:
                ax.set_extent(extents[i])
        
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
        
        if title_on==True:
            title1 = ax.text(tl1[0],tl1[1],plot_main_title,transform=ax.transAxes,fontsize=23, weight='bold',style='italic')
            title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(pressure['time'].attrs['grads_min'])),transform=ax.transAxes,fontsize=17,style='italic')
            #title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=18,style='italic')
            title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=18,weight='heavy',style='italic')
            title5 = ax.text(tl5[0],tl5[1], owner_name,transform=ax.transAxes, size=18,zorder=17,style='italic',
    
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

    
def temp_rh_cross_aegean(time_on, temp, hum, 
                         lon_ave=False, hourly=3, world_map=False, 
                      save_where='temp_rh_cross{}.png', title_on=False
                      ,owner_name='Kutay&Berkay DONMEZ',
     plot_main_title=''
                     , breaking=True,
                     left=0.07, width =  0.65,
                    bottom = 0.6,
                    height = 0.280, 
        tl1=[0,1.04], tl2=[0,1.0080], 
                     tl3=[0.5,1.0080], tl4=[0.77000,1.0080], tl5=[0.0050, 0.9700]):
    """
    Returns cross section of either averaged longitude with pre-indicated 2 point latitude or
            cross section of either averaged latitude with pre-indicated 2 point longitude
            using lon_ave=False or True option;
                        if lon_ave=False returns lat averaged cross section.
    
    if world_map is true the second axis will not be plotted.
    
    Using left-width-bottom-height, if world_map is activated,  one can change its positional arguments
    Using tl's, if the title_on=True,  one can change the positions of titles if they are not satisfied on default
            
    Impotant:Provide lon, lat and height all together
    """
    #define starting time
    start_time_all = datetime.now()
    
    #warn user to only input xarray dataset as variables
    try:
        temperature = temp.sel(time=temp['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
        
    try:
        rhum = hum.sel(time=hum['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
    #indicat lon and lat
    lon_iso = temp.lon[:].values
    lat_iso = temp.lat[:].values
    height_iso = temp.lev[:].values
    
    #copy the data just in case:
    copy_data = temp.copy()
    
    if lon_ave == True:
        temp = temp.mean(dim='lon')
        hum = hum.mean(dim='lon')
        titleis = 'Lon Averaged'
    elif lon_ave == False:
        temp = temp.mean(dim='lat')
        hum = hum.mean(dim='lat')
        titleis = 'Lat Averaged'
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
        
        #if lon_ave true pass lat_iso to contours
        if lon_ave == True:
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
        
        #if lon_ave false pass lon_iso to contours
        if lon_ave == False:
            #contour our temperature
            mesh_temp=ax.contour(lon_iso,height_iso, temperature ,tm, cmap=mymap ,
                        linestyles='solid' , linewidths=0.8)
            ax.clabel(mesh_temp, fontsize=16, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True )
    
            #contour our humidity
            mesh_rh=ax.contour(lon_iso,height_iso, rhum ,r, colors='green' ,
                        linestyles='solid' , linewidths=0.4)
            ax.clabel(mesh_rh, fontsize=12, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True  )
            
            #mesh our humidity
            mesh_hum=ax.contourf(lon_iso,height_iso,rhum ,r,cmap='Greens',extend='both', )
                            
            #label and set size of our axeses
            plt.ylabel('Pressure(hPa)', fontsize=16,weight='heavy',style='italic')
            plt.xlabel('Longitude(°E)', fontsize=16,weight='heavy',style='italic')
            ax.tick_params(axis='y', labelsize=14)
            ax.tick_params(axis='x', labelsize=14)
            
            #invert y axis with pressure decreasing upward
            ax.invert_yaxis()
        
        #arrange the titles of map
        if title_on == True:
            title = ax.text(tl1[0],tl1[1], titleis+' '+plot_main_title, color='navy',transform=ax.transAxes,fontsize=17, weight='bold',style='italic')
            title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(temp['time'].attrs['grads_min'])),transform=ax.transAxes,fontsize=17,style='italic')
            #title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=15,style='italic')
            title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=15,weight='heavy',style='italic')
            title5 = ax.text(tl5[0],tl5[1], owner_name, transform=ax.transAxes, size=15,zorder=17,style='italic',
    
    
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
        
        
        left_h = left+width+0.0305
        rect_box = [left_h, bottom, 0.21, height]
        
        #if only world_map=True make second axis if not do not..
        #set second axes
        if world_map == True:
            
            ax2 = plt.axes(rect_box,projection=cartopy.crs.Mercator())
                            
            #provide sets to not seen
            ax2.get_yaxis().set_ticks([])
            ax2.get_xaxis().set_ticks([])
            
            copy_east = copy_data['lon'].values[0]
            copy_west = copy_data['lon'].values[-1]
            
            copy_south = copy_data['lat'].values[0]
            copy_north = copy_data['lat'].values[-1]
            #define map using cartopy for second axes 
            ax2.add_feature(cartopy.feature.BORDERS.with_scale('10m') , linewidths = 0.5)
            ax2.add_feature(cartopy.feature.COASTLINE.with_scale('10m') , linewidths=0.9)
            ax2.add_feature(cartopy.feature.LAND.with_scale('10m') ,zorder=0,facecolor='brown')
            
            #checking if longitude is between 180 and 360 will change it to negative west values.
            if copy_east>180 or copy_west>180:
                copy_east+=-360
                copy_west+=-360
            
            
            ax2.set_extent([copy_east-1.5,copy_west+1.5,
                                copy_south-1.5,copy_north+1.5])
            
            #show the cross section area in the second axis map
            ax2.plot([copy_east,copy_east],[copy_south,copy_north], c='k',transform = cartopy.crs.PlateCarree())
            ax2.plot([copy_west,copy_west],[copy_south,copy_north], c='k',transform = cartopy.crs.PlateCarree())
            ax2.plot([copy_east,copy_west],[copy_south,copy_south], c='k',transform = cartopy.crs.PlateCarree())
            ax2.plot([copy_east,copy_west],[copy_north,copy_north], c='k',transform = cartopy.crs.PlateCarree())
            
            ax2.scatter([copy_east,copy_east],[copy_south,copy_north], c='k',transform = cartopy.crs.PlateCarree())
            ax2.scatter([copy_west,copy_west],[copy_south,copy_north], c='k',transform = cartopy.crs.PlateCarree())
            ax2.scatter([copy_east,copy_west],[copy_south,copy_south], c='k',transform = cartopy.crs.PlateCarree())
            ax2.scatter([copy_east,copy_west],[copy_north,copy_north], c='k',transform = cartopy.crs.PlateCarree())


        #save our figure
        plt.savefig(save_where.format(t) , bbox_inches='tight')
        
        #infrom user map count going on
        say+=1
        print('Temp_rh_cross | {}.map | Done--{}'.format(say,datetime.now().time()))

        if breaking == True:
            break







    end_time_all = datetime.now()
    print('TEMP_PRESS_TURKEY | TOTAL JOB DONE | Duration: {}'.format(end_time_all - start_time_all))
    
    
def height_pressure(time_on, pressure, height,pr_height ,place='europe',
                     hourly=3, 
                      save_where='wind_pressure_rh{}.png',title_on=False
                      ,owner_name='Kutay&Berkay DONMEZ',
     plot_main_title=''
                     , breaking=True, tl1=[0,1.02], tl2=[0,1.0050], 
                     tl3=[0.5,1.0050], tl4=[0.81000,1.0050], tl5=[0.0047, 0.98422]):
    """ Returns a pre-prepared height-MSL pressure- plot
        
    time_on=indicates the count of maps(hours) will be plotted
    extent:
    
    pr_height(string)=indicates which pressure surface height will be drawn (850,500,700mb are valid)
        
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans'])
    
    If title_on=False the titles will not be seen, unless the title_on=True,
    Default is False.
    
    NOTE:Please Input Xarray DataArray
    """
    
    #warn user to only input xarray dataset as variables
    try:
        press = pressure.sel(time=pressure['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
        
    try:
        geo = height.sel(time=height['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
    
    
    
    #defining lon and lat
    lon_iso = pressure.lon[:].values
    lat_iso = pressure.lat[:].values
    
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans','indianocean','northatlantic'])
    
    #extents corresponding to the places defined
    extents = np.array([[0, 48, 30, 60],[218,318,-5,55],
                        [80,180,-36,5],[260,285,17,33],[275,300,17,33],[30, 130,-20,20],
                        [300, 359,43,64]])
        
    #define starting time
    start_time_all = datetime.now()

    #define our loop ingredients
    toplam=0
    say=0
    for t in range(time_on):
        #define variables
        press = pressure.sel(time=pressure['time'][t] ) 
        geo = height.sel(time=height['time'][t] ) 
        


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
        for i in range(len(places)):
            if place == places[i]:
                ax.set_extent(extents[i])
        
        #define a colormap
        c2 = plt.cm.winter(np.linspace(0., 1, 256))
        c3 = plt.cm.autumn_r(np.linspace(0., 1, 256))
        c1 = plt.cm.Greys_r(np.linspace(0., 1, 256))
        c4 = plt.cm.RdPu_r(np.linspace(0., 1, 256))


        cols = np.vstack((c1,c2,c3,c4))
        mymap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', cols)

        #define our arranges of variables will be ploted
        tm_pressure = np.arange(920,1051,2)
        
        #check which pressure surface is specified
        if pr_height == '850':
            tm_height =  np.arange(1080,1740,30)
        if pr_height == '700':
            tm_height =  np.arange(2640,3310,30)
        if pr_height == '500':
            tm_height =  np.arange(4680,6121,30)
        
        #gridline
        ax.gridlines()
       
        #contourplot for MSLP
        mesh_press=ax.contour(lon_iso, lat_iso, press, tm_pressure, transform = cartopy.crs.PlateCarree(), colors='k' ,
                   linestyles='solid', linewidths=0.9)

        ax.clabel(mesh_press, fontsize=18, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , )
        
        #contourplot for height
        mesh_height=ax.contour(lon_iso, lat_iso, geo, tm_height, colors='white', transform = cartopy.crs.PlateCarree() ,
                   linestyles='solid' , linewidths=1.2)

        ax.clabel(mesh_height, fontsize=20, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , )
        
        #meshplot for wind speed
        mesh_geo=ax.contourf(lon_iso, lat_iso, geo ,tm_height, cmap=mymap, extend='both', alpha=0.6,
                                transform = cartopy.crs.PlateCarree())
        

        
        #make title
        if title_on==True:
            title1 = ax.text(tl1[0],tl1[1],plot_main_title,transform=ax.transAxes,fontsize=23, weight='bold',style='italic')
            title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(pressure['time'].attrs['grads_min'])),transform=ax.transAxes,fontsize=17,style='italic')
            #title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=18,style='italic')
            title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=18,weight='heavy',style='italic')
            title5 = ax.text(tl5[0],tl5[1], owner_name,transform=ax.transAxes, size=18,zorder=17,style='italic',
    
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
        #cb = plt.colorbar(mesh2,fraction=0.1 , pad=0.001, orientation='horizontal' )

        #cb.ax.tick_params(labelsize=17)
        
        #save the fig
        plt.savefig(save_where.format(t) , bbox_inches='tight')
        
        #inform user map count going
        say+=1
        print('height_pressure | {}.map | Done--{}'.format(say,datetime.now().time()))



        if breaking == True:
            break




    end_time_all = datetime.now()
    print('height_pressure | TOTAL JOB DONE | Duration: {}'.format(end_time_all - start_time_all))


def wind_gust(time_on, gust ,place='europe',
                    hourly=3, save_where='gust{}.png',
                    title_on=False,
                    owner_name='Kutay&Berkay DONMEZ',
                    plot_main_title='',
                    breaking=True, tl1=[0,1.02], tl2=[0,1.0050], 
                    tl3=[0.5,1.0050], tl4=[0.81000,1.0050], 
                    tl5=[0.0047, 0.98422]):
    
    """ Returns a pre-prepared wind_gust plot
        
    time_on(int)=indicates the count of maps(hours) will be plotted
    
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans'])
    
    If title_on=False the titles will not be seen, unless the title_on=True,
    Default is False.
    
    NOTE:Please Input Xarray DataArray
    """
    
    #warn user to only input xarray dataset as variables
    try:
        wgust = gust.sel(time=gust['time'][0] ) 
    except:
        raise('Please Input a proper Xarray DataArray')
        
    
    
    #defining lon and lat
    lon_iso = gust.lon[:].values
    lat_iso = gust.lat[:].values
    
    #places avaliable for plotting
    places= np.array(['europe','northamerica','australia','gulfofmexico','carribeans','indianocean','northatlantic'])
    
    #extents corresponding to the places defined
    extents = np.array([[0, 48, 30, 60],[218,318,-5,55],
                        [80,180,-36,5],[260,285,17,33],[275,300,17,33],[30, 130,-20,20],
                        [300, 359,43,64]])
        
    #define starting time
    start_time_all = datetime.now()

    #define our loop ingredients
    toplam=0
    say=0
    for t in range(time_on):
        #define variables
        wgust = gust.sel(time=gust['time'][t] ) 
        
        wgust = xr.where(wgust>0,wgust,0)



        #define valid time using the time dim of the var
        valid = gust['time'][t].values 
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
        for i in range(len(places)):
            if place == places[i]:
                ax.set_extent(extents[i])
        
        #define a colormap
        cmap='gnuplot2'

        #define our arranges of variables will be ploted
        tm_gust = np.arange(0 , 46 , 1)
        
        
        #gridline
        ax.gridlines()
       
        
        #meshplot for wind gust
        mesh_gust=ax.contourf(lon_iso, lat_iso, wgust ,tm_gust, cmap=cmap, extend='both',
                                  norm=mpl.colors.Normalize(vmin=0, vmax=45),
                                transform = cartopy.crs.PlateCarree())
        

        
        #make title
        if title_on==True:
            title1 = ax.text(tl1[0],tl1[1],plot_main_title,transform=ax.transAxes,fontsize=23, weight='bold',style='italic')
            title2 = ax.text(tl2[0],tl2[1],'Init: {}'.format(str(gust['time'].attrs['grads_min'])),transform=ax.transAxes,fontsize=17,style='italic')
            #title3 = ax.text(tl3[0],tl3[1],'Hour: {}'.format(toplam),transform=ax.transAxes,fontsize=18,style='italic')
            title4 = ax.text(tl4[0],tl4[1],'Valid: {}'.format(valid),transform=ax.transAxes,fontsize=18,weight='heavy',style='italic')
            title5 = ax.text(tl5[0],tl5[1], owner_name,transform=ax.transAxes, size=18,zorder=17,style='italic',
    
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
        
        #indicating text intervals with respect to given area
        ara = 8
        if place == 'northamerica' or place == 'australia' or 'indianocean' or 'northatlantic':
            ara = 14
        
        
        for i in wgust['lat'][0:-17:ara]:
            for j in wgust['lon'][0:-1:ara]:
                if int(np.round(wgust.sel(lat=i, lon=j).values)) == 0:
                    pass
                else:
                    text = ax.text(j, i, int(np.round(wgust.sel(lat=i, lon=j).values)),
                               ha="center", va="center", color="w",transform = cartopy.crs.PlateCarree(), size=20)
                
        #define our colorbar
        #cb = plt.colorbar(mesh2,fraction=0.1 , pad=0.001, orientation='horizontal' )

        #cb.ax.tick_params(labelsize=17)
        
        #save the fig
        plt.savefig(save_where.format(t) , bbox_inches='tight')
        
        #inform user map count going
        say+=1
        print('wind_gust | {}.map | Done--{}'.format(say,datetime.now().time()))



        if breaking == True:
            break




    end_time_all = datetime.now()
    print('wind_gust | TOTAL JOB DONE | Duration: {}'.format(end_time_all - start_time_all))
