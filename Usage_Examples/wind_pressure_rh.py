#!/usr/bin/env python
# coding: utf-8

# In[5]:


from visjobs.datas import get_data
data = get_data.pick_data( hour='12',latest=True,model='GFS', hourly=False)

from visjobs.visualize import draw_map

press = data['prmslmsl'][0:30:1,:,:].sel(lat = slice(30,65) ,lon = slice(0,48)) / 100
ugrd =  data['ugrd10m'][0:30:1,:,:].sel(lat = slice(30,65) ,lon = slice(0,48)) * 1.94384449
vgrd =  data['vgrd10m'][0:30:1,:,:].sel(lat = slice(30,65) ,lon = slice(0,48)) * 1.94384449
rh =  data['rhprs'][0:30:1,:,:].sel(lat = slice(30,65) ,lon = slice(0,48), lev=700) 
time = len(data['time'][0:30:1])

lon_iso =press.lon[:]
lat_iso = press.lat[:]


# In[6]:


from pylab import rcParams
rcParams['figure.figsize'] = 21,24
draw_map.wind_pressure_rh(time, press, rh, ugrd, vgrd, lon_iso, lat_iso, extent=[0, 48, 30, 60], 
                          save_where='Pictures\wind_pressure_rh{}.png', breaking=False )


# In[ ]:




