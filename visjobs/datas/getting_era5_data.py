"""By Kutay Dönmez"""

from siphon.catalog import TDSCatalog
import matplotlib.pyplot as plt
import numpy as np
from siphon.http_util import session_manager
from datetime import datetime,timedelta
import xarray as xr

def get_yearmonth_era5(username, password, date, var, hr, coords=[20,47,30,50]):
    session_manager.set_session_options(auth=(username, password))
    cat = TDSCatalog('https://rda.ucar.edu/thredds/catalog/files/g/ds633.0/e5.oper.an.pl/{}/catalog.xml'
                     .format(date[:6]))
    datasetName = "e5.oper.an.pl.128_060_{}.ll025sc.{}00_{}23.nc".format(var, date, date)  
    ds = catalog.datasets[datasetName]    
    dates = '20180101'
    f = ds.subset()
    query = f.query()
    query.lonlat_box(north=coords[3], south=coords[2], east=coords[1], west=coords[0])
    start = datetime(int(dates[:4]),int(dates[4:6]),int(dates[6:]))
    end   = start + timedelta(hours=hr) 
    query.time_range(start,end)
    query.accept('netcdf4')
    query.variables('all')
    data = f.get_data(query)
    return data

def get_era5(data, date, coords=[20,47,30,50]):
    """interval must be given as yearmonthday such as 20180101 as str
       variable: desired variable
       interval: time interval in the form of indicated above"""
    
    v1 = list(data.variables.keys())[-1]
    temp_var = data.variables[v1]
    time_var = data.variables['time']
    lat_var = data.variables['latitude']
    lon_var = data.variables['longitude']
    lev_var = data.variables['level']
    temp_vals = np.array(temp_var)
    lat_vals = np.array(lat_var)
    lon_vals = np.array(lon_var)
    lev_vals = np.array(lev_var)
    time_vals = time_var[:].squeeze()
    date = datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
    time_vals = np.array(time_var[:])
    tm_list = []
    for i in time_vals:
        i = i.astype('float64')
        tm = datetime(1900,1,1) + timedelta(hours=i)
        tm_list.append(tm)
    xr_dt = xr.Dataset({'{}'.format(v1): (['time','isobaric', 'latitude', 'longitude'],  temp_vals) },
                                coords={  'time'     : tm_list,
                                          'isobaric' : lev_vals,
                                          'latitude' : lat_vals,
                                          'longitude': lon_vals,
                                         })
    
            
    
    
    return xr_dt