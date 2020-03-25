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