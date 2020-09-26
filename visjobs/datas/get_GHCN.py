import pandas as pd
import numpy as np
from ftplib import FTP

"""
Functions Derived from,

        https://gitlab.com/nedcr
        
        and
        
        https://github.com/jjrennie/GHCNpy/blob/master/ghcnpy/iotools.py
"""

# Metadata specs #

metadata_col_specs = [
    (0,  12),
    (12, 21),
    (21, 31),
    (31, 38),
    (38, 41),
    (41, 72),
    (72, 76),
    (76, 80),
    (80, 86)
]

metadata_names = [
    "ID",
    "LATITUDE",
    "LONGITUDE",
    "ELEVATION",
    "STATE",
    "NAME",
    "GSN FLAG",
    "HCN/CRN FLAG",
    "WMO ID"]

metadata_dtype = {
    "ID": str,
    "STATE": str,
    "NAME": str,
    "GSN FLAG": str,
    "HCN/CRN FLAG": str,
    "WMO ID": str
    }


# Data specs #

data_header_names = [
    "ID",
    "YEAR",
    "MONTH",
    "ELEMENT"]

data_header_col_specs = [
    (0,  11),
    (11, 15),
    (15, 17),
    (17, 21)]

data_header_dtypes = {
    "ID": str,
    "YEAR": int,
    "MONTH": int,
    "ELEMENT": str}

data_col_names = [[
    "VALUE" + str(i + 1),
    "MFLAG" + str(i + 1),
    "QFLAG" + str(i + 1),
    "SFLAG" + str(i + 1)]
    for i in range(31)]
# Join sub-lists
data_col_names = sum(data_col_names, [])

data_replacement_col_names = [[
    ("VALUE", i + 1),
    ("MFLAG", i + 1),
    ("QFLAG", i + 1),
    ("SFLAG", i + 1)]
    for i in range(31)]
# Join sub-lists
data_replacement_col_names = sum(data_replacement_col_names, [])
data_replacement_col_names = pd.MultiIndex.from_tuples(
    data_replacement_col_names,
    names=['VAR_TYPE', 'DAY'])

data_col_specs = [[
    (21 + i * 8, 26 + i * 8),
    (26 + i * 8, 27 + i * 8),
    (27 + i * 8, 28 + i * 8),
    (28 + i * 8, 29 + i * 8)]
    for i in range(31)]
data_col_specs = sum(data_col_specs, [])

data_col_dtypes = [{
    "VALUE" + str(i + 1): int,
    "MFLAG" + str(i + 1): str,
    "QFLAG" + str(i + 1): str,
    "SFLAG" + str(i + 1): str}
    for i in range(31)]
data_header_dtypes.update({k: v for d in data_col_dtypes for k, v in d.items()})

def read_ghcn_data_file(filename):
    """Reads in all data from a GHCN .dly data file

    :param filename: path to file
    :param variables: list of variables to include in output dataframe
        e.g. ['TMAX', 'TMIN', 'PRCP']
    :returns: Pandas dataframe
    """

    df = pd.read_fwf(
        filename,
        colspecs=data_header_col_specs + data_col_specs,
        names=data_header_names + data_col_names,
        index_col=data_header_names,
        dtype=data_header_dtypes
        )

    df.columns = data_replacement_col_names

    
    df = df.loc[:, ('VALUE', slice(None))]
    df.columns = df.columns.droplevel('VAR_TYPE')

    df = df.stack(level='DAY').unstack(level='ELEMENT')

    
    df.replace(-9999.0, pd.np.nan, inplace=True)
    df.dropna(how='all', inplace=True)

    # replace the entire index with the date.
    # This loses the station ID index column!
    # This will usuall fail if dropna=False, since months with <31 days
    # still have day=31 columns
    df.index = pd.to_datetime(
        df.index.get_level_values('YEAR') * 10000 +
        df.index.get_level_values('MONTH') * 100 +
        df.index.get_level_values('DAY'),
        format='%Y%m%d')
    
    df['TAVG'] = df['TAVG'] / 10
    df['TMIN'] = df['TMIN'] / 10
    df['TMAX'] = df['TMAX'] / 10
    df['PRCP'] = df['PRCP'] / 10
    return df


# Reading functions #
def get_turkey_ID():
    dt = pd.read_csv(r'Turkey_Stations_ID.csv')
    for i in range(len(dt)):
        print('ID ', 'for ', 'station ', '{} : '.format(dt['Station'][i]), '{}'.format(dt['ID'][i]))

def get_data_with_station(station_id):
    """ 
    *** Returns Pandas DataFrame ***
    
    Please Input Station ID: (String)"""
    print("\nGETTING DATA FOR STATION: ",station_id)

    ftp = FTP('ftp.ncdc.noaa.gov')
    ftp.login()
    ftp.cwd('pub/data/ghcn/daily/all')
    ftp.retrbinary('RETR '+station_id+'.dly', open(station_id+'.dly', 'wb').write)
    ftp.quit()

    outfile=station_id+".dly"
    
    dt = read_ghcn_data_file(filename=outfile)
    print('{} STATION DATA IS TAKEN'.format(station_id))
    return dt