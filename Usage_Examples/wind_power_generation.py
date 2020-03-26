#!/usr/bin/env python
# coding: utf-8

from visjobs.datas import get_data
from visjobs.windenergy import wind_parameters

data = get_data.pick_data( year='2020', month='03', day='24', hour='12',latest=False,model='GFS', hourly=False)

#variables
A = 5281 #m2
R = 286.7 # N*m /(mol*K)
cp=0.59
prs80 = 100367.63 #Pa


# here we are getting the desired variables with desired areas of interest,returned in dictionary
time, area_dict = get_data.pick_area(data, total_process=2, interval=1, list_of_vars=['tmp80m','ugrd80m','vgrd80m'],
                                     pr_height=[1000,500],
                          list_of_areas=['australia','europe'])

tmp80m = area_dict['australia'][0]
uwind80 = area_dict['australia'][1]
vwind80 = area_dict['australia'][2]


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




