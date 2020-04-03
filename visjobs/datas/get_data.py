# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8
import xarray as xr
from datetime import datetime,timedelta
import numpy as np
from netCDF4 import num2date
import numpy as np

#learn if the latest wanted or the desired date from user?
def pick_data(year=None, month=None, day=None, hour=None, latest=False, model='GFS', hourly=False, resolution=0.25):
    
    
    #multiply resolution with 10
    resolution = int(np.multiply(resolution,100))
    
    #indicate available models
    models = np.array(['GFS', 'NAM'])
    
    #available times
    hours = np.array(['18','12','06','00'])
    
    #check user only inputs hourly and GFS together not any else option 
    if hourly == True and model=='NAM':
        print('Error --> model=NAM and hourly=NAM choices can not be done together..')
        raise
    
    #Now if model is models[0] get the relevant data querying if latest agreement or specified date.
    if model == models[0]:
        if latest==True:
            # get the latest year,month,day
            time = datetime.utcnow()
            year = str(time.year)
            month = time.month
            day=time.day
            if month<10:
                month = str(0)+str(month)
            if day<10:
                day = str(0)+ str(day)
            if hourly == False:
            
            #check which hour of model is run latest.First checking 18Z if exists
            
                data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}/gfs{}/gfs_0p{}_{}z'.
                                       format(resolution, str(year)+str(month)+str(day), resolution, hour))
            elif hourly == True:
            
                data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}_1hr/gfs{}/gfs_0p{}_1hr_{}z'.
                                       format(resolution, str(year)+str(month)+str(day), resolution, hour))
                 
        #this case date is already is given
        elif latest==False:
           
            if hourly == False:
                data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}/gfs{}/gfs_0p{}_{}z'.
                                       format(resolution, str(year)+str(month)+str(day), resolution, str(hour)))
            elif hourly == True:
                data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}_1hr/gfs{}/gfs_0p{}_1hr_{}z'.
                                       format(resolution, str(year)+str(month)+str(day), resolution, str(hour)))
                
    
    elif model == models[1]:
        if latest==True:
            # get the latest year,month,day
            time = datetime.utcnow()
            year = str(time.year)
            month = time.month
            day=time.day
            if month<10:
                month = str(0)+str(month)
            if day<10:
                day = str(0)+ str(day)
            
            #check which hour of model is run latest.First checking 18Z if exists
            
            data = xr.open_dataset(r'https://nomads.ncep.noaa.gov:9090/dods/nam/nam{}/nam_{}z'.
                                       format(str(year)+str(month)+str(day), hour))
                   
        #this case, date is already is given
        elif latest==False:
            
            data = xr.open_dataset(r'https://nomads.ncep.noaa.gov:9090/dods/nam/nam{}/nam_{}z'.
                                       format(str(year)+str(month)+str(day),str(hour)))
                
        

    return data

#now with this function we will be able to specifize the area we are interested and also the variables.
def pick_area(data ,total_process, interval ,list_of_vars, list_of_areas, init_time=0, pr_height=None, ):
    """ Returns time_with_interval and the dictionary of the areas with variables
        data = NAM or GFS xarray DataArray should be given
        total_process = (int) means the until which time step data is expected (1 or 2 or 100 etc.)
        interval = (int) means until the expected time step in which interval it should go.
        list_of_vars = the list of variables can be also a single element list:
                                the variable names can be found at:
                                https://nomads.ncep.noaa.gov:9090/dods/gfs_0p25/gfs20200326/gfs_0p25_06z_anl.info
                                
        list_of_areas = the list of areas can be also a single element: available options:
                -->['europe','northamerica','australia','gulfofmexico','carribeans','indianocean']
    """
    
    
    
    #trying if the longitude values from 0 to 360 or -180 to 180?
    
    if data['tmp2m']['lon'].values[0] < 0:
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [-142,-42,0,60],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [-100,-75,18,31],
              'carribeans' : [-85,-60,12,38], 
              'indianocean' : [30, 130,-35,35],
              'northatlantic' : [-60, -1,43,90]}
                                                                  
    # -180 to 180 change the values given in the dictionary to relevant
    else:
        #places avaliable for return its data
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [218,318,-10,70],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [260,285,14,37],
              'carribeans' : [275,300,12,38], 
              'indianocean' : [30, 130,-35,35],
              'northatlantic' : [300, 359,43,90]}
        
    
    #constructing important list and dict for the loop
    
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