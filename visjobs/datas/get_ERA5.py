"""By Kutay-Berkay DÖNMEZ"""

import xarray as xr
import requests
from pydap.client import open_url
from pydap.cas.urs import setup_session

def get_era5_pressure(username, password, date, var, session):
    vrb = {'pv':'060',
       'crwc':'075',
       'u':'131',
       'v':'132',
       'z':'129',
       'cswc':'076',
       'q':'133',
       'w':'135',
       'vo':'138',
       'd':'155', 
       'r':'157',
       'clwc':'246',
       'ciwc':'247',
       'cc':'248',
       'o3':'203',
       't':'130'}
    
    code = {'pv':'sc',
       'crwc':'sc',
       'u':'uv',
       'v':'uv',
       'z':'sc',
       'cswc':'sc',
       'q':'sc',
       'w':'sc',
       'vo':'sc',
       'd':'sc', 
       'r':'sc',
       'clwc':'sc',
       'ciwc':'sc',
       'cc':'sc',
       'o3':'sc',
       't':'sc'}

    
    #get the url
    ds_url = 'https://rda.ucar.edu/thredds/dodsC/files/g/ds633.0/e5.oper.an.pl/{}/e5.oper.an.pl.128_{}_{}.ll025{}.{}00_{}23.nc'.format(date[:6], vrb[var], var, code[var], date, date)
    
    #access authorization
    store = xr.backends.PydapDataStore.open(ds_url,
                                            session=session)
    #get data
    ds = xr.open_dataset(store,  )
    return ds

def get_pressure_variables(username, password, date, variable_list, parse='all'):
    """Gets all the needed pressure ERA5 variables
    
        PARAMETERS:
        username: cds copernicus climate username (str),
        password: cds copernicus climate password (str),
        date: date (str): in eg. '20050829' format,
        variable list: list of variables that are desired (list of str),
                    available variable options: ['pv',
                                                 'crwc',
                                                 'u',
                                                 'v',
                                                 'z',
                                                 'cswc',
                                                 'q',
                                                 'w',
                                                 'vo',
                                                 'd',
                                                 'r',
                                                 'clwc',
                                                 'ciwc',
                                                 'cc',
                                                 'o3',
                                                 't']
                    
        parse: whether whole data or a part of it is expected: (str) 'all' or 'turkey'
        """
    
    print('Starting Session')
    #start the session
    session = requests.Session()
    session.auth = (username, password)
    variables = variable_list
    dt_list = [] 
    for vr in variables:
        d = get_era5_pressure(username, password, date, vr, session)
        dt_list.append(d)
        print('Variable {} is taken'.format(vr))
    
    if parse == 'all':
        return xr.merge(dt_list)
    
    elif parse == 'turkey':
        turk_lat = slice(50, 30)
        turk_lon = slice(20, 47)
        
        turk_dt_list = []
        for i, vr in enumerate(variables):
            d = dt_list[i].sel(latitude = turk_lat, longitude = turk_lon,)

            turk_dt_list.append(d)
        
        return xr.merge(turk_dt_list)

#era5 single data
def get_era5_single(username, password, date, month, var, session):
    month_day = {'01':'31',
                 '03':'31',
                 '04':'30',
                 '05':'31',
                 '06':'30',
                 '07':'31',
                 '08':'31',
                 '09':'30',
                 '10':'31',
                 '11':'30',
                 '12':'31'}
    
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
    
    cat = 'https://rda.ucar.edu/thredds/dodsC/files/g/ds633.0/e5.oper.an.sfc/{}/'.format(date[:6])
    
    if month in ['01','03','04','05','06','07','08','09','10','11','12']:
        datasetName = "e5.oper.an.sfc.128_{}_{}.ll025sc.{}0100_{}{}23.nc".format(vrb[var], var, date[:6], date[:6], month_day[month])
    
    elif month == '02':
        day_count = monthrange(date[:4], 2)[1]
        datasetName = "e5.oper.an.sfc.128_{}_{}.ll025sc.{}0100_{}{}23.nc".format(vrb[var], var, date[:6], date[:6], str(day_count))
    
    
    ds_url = cat + datasetName
    
    #access authorization
    store = xr.backends.PydapDataStore.open(ds_url,
                                            session=session)
    #get data
    ds = xr.open_dataset(store, )
    return ds

def get_single_variables(username, password, date, variable_list, parse='all'):
    """Gets all the needed single ERA5 variables
        
        PARAMETERS:
        username: cds copernicus climate username (str),
        password: cds copernicus climate password (str),
        date: date (str): in eg. '20050829' format,
        variable list: list of variables that are desired (list of str),
                    available variable options: ['aluvp',
                                                 'aluvd',
                                                 'alnip',
                                                 'alnid',
                                                 'ci',
                                                 'asn',
                                                 'rsn',
                                                 'istl1',
                                                 'istl2',
                                                 'istl3',
                                                 'istl4',
                                                 'swvl1',
                                                 'swvl2',
                                                 'swvl3',
                                                 'swvl4',
                                                 'cape',
                                                 'lailv',
                                                 'laihv',
                                                 'tclw',
                                                 'tciw',
                                                 'sp',
                                                 'tcw',
                                                 'scwv',
                                                 'stl1',
                                                 'sd',
                                                 'chnk',
                                                 'msl',
                                                 'blh',
                                                 'tcc',
                                                 '10u',
                                                 '10v',
                                                 '2t',
                                                 '2d',
                                                 'stl2',
                                                 'stl3',
                                                 'lcc',
                                                 'mcc',
                                                 'hcc',
                                                 'src',
                                                 'tco3',
                                                 'iews',
                                                 'inss',
                                                 'ishf',
                                                 'ie',
                                                 'skt',
                                                 'stl4',
                                                 'tsn',
                                                 'fal',
                                                 'fsr',
                                                 'flsr']
                    
        parse: whether whole data or a part of it is expected: (str) 'all' or 'turkey'"""
    
    print('Starting Session')
    #start the session
    session = requests.Session()
    session.auth = (username, password)
    
    month = date[4:6]
    start_dt = '{}-{}-{}T00:00:00.000000000'.format(date[:4], date[4:6], date[6:8])
    end_dt = '{}-{}-{}T23:00:00.000000000'.format(date[:4], date[4:6], date[6:8])
        
    variables = variable_list
    dt_list = [] 
    for vr in variables:
        d = get_era5_single(username, password, date, month, vr, session)
        d = d.sel(time = slice(start_dt, end_dt))
        dt_list.append(d)
        print('Variable {} is taken'.format(vr))
    
    if parse == 'all':
        return xr.merge(dt_list)
    
    elif parse == 'turkey':
        
        turk_lat = slice(50, 30)
        turk_lon = slice(20, 47)
        
        turk_dt_list = []
        for i, vr in enumerate(variables):
            d = dt_list[i].sel(latitude = turk_lat, longitude = turk_lon, time = slice(start_dt, end_dt))
            turk_dt_list.append(d)
        
        return xr.merge(turk_dt_list)