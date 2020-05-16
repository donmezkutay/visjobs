"""By Kutay Dönmez"""

from siphon.catalog import TDSCatalog
from siphon.http_util import session_manager
import xarray as xr
import numpy as np
import netCDF4
from datetime import datetime
from datetime import timedelta

def get_yearmonth_era5(username, password, date):
    session_manager.set_session_options(auth=(username, password))
    cat = TDSCatalog('https://rda.ucar.edu/thredds/catalog/files/g/ds633.0/e5.oper.an.pl/{}/catalog.html'
                     .format(date))
    return cat

def get_era5(variable, username, password, date, coords=[20,47,30,50]):
    """interval must be given as yearmonthday such as 20180101 as str
       variable: desired variable
       interval: time interval in the form of indicated above"""
    cat = get_yearmonth_era5(username, password, date[:6])
    for i in range(len(list(cat.datasets))):
        
        data_list = []
        if len(variable) == 2:
            dt_var = str(cat.datasets[i])[-36:-34]
            dt_time = str(cat.datasets[i])[-25:-17]
        elif len(variable) == 4:
            dt_var = str(cat.datasets[i])[-38:-34]
            dt_time = str(cat.datasets[i])[-25:-17]
        elif len(variable) == 3:
            dt_var = str(cat.datasets[i])[-37:-34]
            dt_time = str(cat.datasets[i])[-25:-17]
        elif len(variable) == 1:
            dt_var = str(cat.datasets[i])[-35:-34]
            dt_time = str(cat.datasets[i])[-25:-17]
        
        if dt_var == variable and dt_time == date:
            
            best_ds = cat.datasets[i]
            ncss = best_ds.subset()
            query = ncss.query()
            query.lonlat_box(north=50, south=30, east=47, west=20)
            start = datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
            end   = start + timedelta(hours=23) 
            query.time_range(start,end)
            query.accept('netcdf4')
            query.variables('all')
            data = ncss.get_data(query)
            #data = xr.Dataset(data)
            v1 = list(data.variables.keys())[-2]
            temp_var = data.variables[v1]
            time_var = data.variables['time']
            lat_var = data.variables['latitude']
            lon_var = data.variables['longitude']
            lev_var = data.variables['isobaric']
            temp_vals = np.array(temp_var)
            lat_vals = np.array(lat_var)
            lon_vals = np.array(lon_var)
            lev_vals = np.array(lev_var)
            time_vals = time_var[:].squeeze()
            date = datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
            tm_list = []
            for i in time_vals:
                tm = date + timedelta(hours=i)
                tm_list.append(tm)
            print(tm_list)
            xr_dt = xr.Dataset({'{}'.format(variable): (['time','isobaric', 'latitude', 'longitude'],  temp_vals) },
                                coords={  'time'     : tm_list,
                                          'isobaric' : lev_vals,
                                          'latitude' : lat_vals,
                                          'longitude': lon_vals,
                                         })
            
    
    return xr_dt