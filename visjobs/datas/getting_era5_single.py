"""By Kutay Dönmez"""

from siphon.catalog import TDSCatalog
import matplotlib.pyplot as plt
import numpy as np
from siphon.http_util import session_manager
from datetime import datetime,timedelta
import xarray as xr
from calendar import monthrange


def get_yearmonth_era5(username, password, date, var, hr , month, coords=[20,47,30,50]):
    month_day = {'january':'31',
                 'march':'31',
                 'april':'30',
                 'may':'31',
                 'june':'30',
                 'july':'31',
                 'august':'31',
                 'september':'30',
                 'october':'31',
                 'november':'30',
                 'december':'31'}
    
    vrb = {'aluvp':'015',
           'aluvd':'016',
           'alnip':'017',
           'alnid':'018',
           'ci':'031',
           'asn':'032', 
           'rsn':'033',
           'sstk':'034',
           'istl1':'035',
           'istl2':'036',
           'istl3':'037',
           'istl4':'038',
           'swvl1':'039',
           'swvl2':'040',
           'swvl3':'041',
           'swvl4':'042',
           'cape':'059',
           'lailv':'066',
           'laihv':'067',
           'tclw':'078',
           'tciw':'079',
           'sp':'134',
           'tcw':'136',
           'scwv':'137',
           'stl1':'139',
           'sd':'141',
           'chnk':'148',
           'msl':'151',
           'blh':'159',
           'tcc':'164',
           '10u':'165',
           '10v':'166',
           '2t':'167',
           '2d':'168',
           'stl2':'170',
           'stl3':'183',
           'lcc':'186',
           'mcc':'187',
           'hcc':'188',
           'src':'198',
           'tco3':'206',
           'iews':'229',
           'inss':'230',
           'ishf':'231',
           'ie':'232',
           'skt':'235',
           'stl4':'236',
           'tsn':'238',
           'fal':'243',
           'fsr':'244',
           'flsr':'245'
            }
       
    
    session_manager.set_session_options(auth=(username, password))
    cat = TDSCatalog('https://rda.ucar.edu/thredds/catalog/files/g/ds633.0/e5.oper.an.sfc/{}/catalog.xml'
                     .format(date[:6]))
    
    if date[4:6] in ['01','03','04','05','06','07','08','09','10','11','12']:
        datasetName = "e5.oper.an.sfc.128_{}_{}.ll025sc.{}0100_{}{}23.nc".format(vrb[var], var, date[:6], date[:6], month_day[month])
    
    elif date[4:6] == '02':
        day_count = monthrange(date[:4], 2)[1]
        datasetName = "e5.oper.an.sfc.128_{}_{}.ll025sc.{}0100_{}{}23.nc".format(vrb[var], var, date[:6], date[:6], str(day_count))
        
    ds = cat.datasets[datasetName]    
    f = ds.subset()
    query = f.query()
    query.lonlat_box(north=coords[3], south=coords[2], east=coords[1], west=coords[0])
    start = datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
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
    temp_vals = np.array(temp_var)
    lat_vals = np.array(lat_var)
    lon_vals = np.array(lon_var)
    time_vals = time_var[:].squeeze()
    date = datetime(int(date[:4]),int(date[4:6]),int(date[6:]))
    time_vals = np.array(time_var[:])
    tm_list = []
    for i in time_vals:
        i = i.astype('float64')
        tm = datetime(1900,1,1) + timedelta(hours=i)
        tm_list.append(tm)
    xr_dt = xr.Dataset({'{}'.format(v1): (['time', 'latitude', 'longitude'],  temp_vals) },
                                coords={  'time'     : tm_list,
                                          'latitude' : lat_vals,
                                          'longitude': lon_vals,
                                         })
    
            
    
    
    return xr_dt