#!/usr/bin/env python
# coding: utf-8

# In[1]:


from visjobs.datas import get_data
from visjobs.windenergy import wind_parameters


# In[3]:


data = get_data.pick_data( year='2020', month='03', day='24', hour='12',latest=False,model='GFS', hourly=False)


# In[4]:


#variables
A = 5281 #m2
R = 286.7 # N*m /(mol*K)
cp=0.59
prs80 = 100367.63 #Pa
tmp80 = data['tmp80m'][:2,:,:].sel(lat = slice(34,43),lon=slice(25,45)) # K
uwind80 = data['ugrd80m'][:2,:,:].sel(lat = slice(34,43),lon=slice(25,45)) # m/s
vwind80 = data['vgrd80m'][:2,:,:].sel(lat = slice(34,43),lon=slice(25,45)) # m/s
lon_iso =uwind80.lon[:].values
lat_iso = uwind80.lat[:].values
time = len(data['time'][:2])


# In[5]:


#calculating density
density = wind_parameters.calculating_density_height(uwind80, vwind80, tmp80, prs80, cp, R)


# In[6]:


#calculating wind speed in m/s from u and v winds
ws = wind_parameters.uv_to_ws(uwind80, vwind80)


# In[7]:


#limiting wind speed values in regard to cut_in, cut_out etc. turbine dependent values
ws_limited = wind_parameters.limiting_wind_speed(ws, cut_in=3, cut_out=25, rated_wind_speed=13)


# In[8]:


power = wind_parameters.calculating_power_output(density, ws_limited, cp, A, rated_power=1.5)


# In[ ]:





# In[ ]:




