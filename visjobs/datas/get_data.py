# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8
import xarray as xr
from datetime import datetime,timedelta
import numpy as np


#learn if the latest wanted or the desired date from user?
def pick_data(year=None, month=None, day=None, hour=None, latest=False, model='GFS', hourly=False, resolution=0.25,
              *args, **kwargs):
    """Returns Xarray Dataset of the relevant atmospheric model data
    
        year       :str;
        month      :str; (eg. Instead of '1' input '01')
        day        :str; (eg. Instead of '1' input '01')
        hour       :str; Options: '18', '12', '06', '00' [Should be given]
        latest     :Boolean (If Latest=True given date is no more importance)
        model      :str; Options: 'GFS', 'NAM', 'GEFS' 
        hourly     :Boolean; (Only valid for GFS Data please choose model=GFS for this feature)
        Resolution :int; (Only valid for GFS Data)"""
    
    #Check if user has passed a valid obligatory hour
    try:
        if hour != None:
            pass
    except:
        print("""Error --> Even If you indicate Latest=True, please input the run hour..
                               Options: '18', '12', '06', '00'
                  """)
        raise
            
    
    #multiply resolution with 10 (only for GFS)
    resolution = int(np.multiply(resolution,100))
    
    #available models
    models = np.array(['GFS', 'NAM', 'GEFS'])
    
    #available hours
    hours = np.array(['18','12','06','00'])
    
    #check user only inputs hourly and GFS together not any else option 
    if model in ['NAM', 'GEFS'] and hourly == True:
        print('Error --> model={} and hourly=True choices can not be done together..'.format(model))
        raise
    
    #Checking if user asking for the latest data, or the user indicates a specific date..
    if latest == True:
        
        # get the latest year,month,day
        time = datetime.utcnow()
        year = str(time.year)
        month = time.month
        day=time.day
        if month<10:
            month = str(0)+str(month)
        if day<10:
            day = str(0)+ str(day)
    
    if latest == False:
        
        
        if year and month and day is not None:
            pass
        
        else:
            print('Error --> Please input year, month and day for latest=False')
            raise
            
        
    #GFS
    if model == models[0]:
        
        if hourly == False:

            data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}/gfs{}/gfs_0p{}_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour), 
                                     *args, **kwargs)
        elif hourly == True:

            data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}_1hr/gfs{}/gfs_0p{}_1hr_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour),
                                     *args, **kwargs)
        
    #NAM
    elif model == models[1]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/nam/nam{}/nam_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
    #GEFS
    elif model == models[2]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gens_bc/gens{}/gep_all_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
            

    return data

#now with this function we will be able to specify the area we are interested and also the variables.
def pick_area(data ,total_process, interval ,list_of_vars, list_of_areas, init_time=0, pr_height=None, ):
    """ Returns time_with_interval and the dictionary of the areas with variables
     
        data          :str; 'GFS', 'NAM' or 'GEFS' Xarray DataArray should be given
        total_process :int; means the until which time step data is expected (1 or 2 or 100 etc.)
        interval      :int; means until the expected time step in which interval data should be taken.
        list_of_vars  :list of str; (Data variable names) the list of variables can be also a single element list:
                                
                                
        list_of_areas :list of str; the list of areas can be also a single element: 
                                    available options:
                                    ['europe','northamerica','australia','gulfofmexico','carribeans','indianocean']
    """
    
    
    
    #trying if the longitude values change from 0 to 360 or -180 to 180?
    
    if data['tmp2m']['lon'].values[0] < 0:
        
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [-142,-42,0,60],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [-100,-75,18,31],
              'carribeans' : [-85,-60,12,38], 
              'indianocean' : [30, 130,-35,35],
              'NH' : [-180, 180 ,0,90]}
                                                                  
    # -180 to 180 change the values given in the dictionary to relevant
    else:
        
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [218,318,-10,70],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [260,285,14,37],
              'carribeans' : [275,300,12,38], 
              'indianocean' : [30, 130,-35,35],
              'NH' : [0, 360 ,0,90]}
        
    
    
    places_dict = {}
    #looping in the list of areas
    say_pl = 1
    for pl in list_of_areas:
        variables_l = []
        #looping in the list of variables
        say_var =1
        for var in list_of_vars:
            #check if data contains 'lev' coords.
            try:
                if len(pr_height) == 1:
                    #wrap the data
                    single = data[var][init_time:total_process:interval, :, :].sel(lon=slice(p_d[pl][0],p_d[pl][1]),  
                                                                          lat=slice(p_d[pl][2],p_d[pl][3]), 
                                                                          lev=pr_height[0])
                elif len(pr_height) == 2:
                    single = data[var][init_time:total_process:interval, :, :].sel(lon=slice(p_d[pl][0],p_d[pl][1]),  
                                                                      lat=slice(p_d[pl][2],p_d[pl][3]), 
                                                                      lev=slice(pr_height[0],pr_height[1]))
                #append a single variable given by the user
               
            
            #if no 'lev' coords exist.
            except:
                single = data[var][init_time:total_process:interval, :, :].sel(lon=slice(p_d[pl][0],p_d[pl][1]),  
                                                                      lat=slice(p_d[pl][2],p_d[pl][3]),)
            
                #append a single variable given by the user
            variables_l.append(single)
        
            
            
        
        #append all the variables with respect to their area of interest.
        places_dict[pl] = variables_l
    
    #time data with interval
    time_w_interval = data['time'][init_time:total_process:interval]
    
    #return
    return len(time_w_interval), places_dict