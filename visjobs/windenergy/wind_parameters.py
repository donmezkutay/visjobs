### !/usr/bin/env python
# coding: utf-8
import xarray as xr
import numpy as np
import matplotlib as mpl
import numpy as np
import metpy.calc as mpcalc
from metpy.units import units

#====================================================================*
#CALCULATIONS FOR THE WIND ENERGY OUPUTS OF ATMOSPHERIC MODELS
#____________________________________________________________________*

#Using the wind speed outputs of our model we are limiting the energy generation 
#availability using basic wind energy rules 
def limiting_wind_speed(ws, cut_in=3, cut_out=25, rated_wind_speed=13):
    """ Returns new arranged DataArray of wind speed considering cut_in, cut_out mechanisms of 
        energy availability..
        
        ws = wind speed in m/s
        cut_in  = Wind speed magnitude under which the generation of energy by wind turbine is not allowed
        cut_out   = Wind speed magnitude over which the generation of energy by wind turbine is shut down for no damage
        --> Both of those variables is related with energy efficiency and performance of the wind turbine
        
        rated_wind_speed = Wind Speed magnitude over which the maximum capacity is reached and turbine will generate same 
                            amount of energyenergy until cut_in value is touched.
        ws_limited = Limited wind speeds (arranged) in considering both cut_in, cut_out values
        
        NOTE : Cut_in and Cut_out values may change with different wind turbines
        IMPORTANT:cut_in, cut_out, rated_wind_speed, rated_power values are unique to the turbine used, can differ.
                    For Default Values "Vestas V82-1.5"  model is used.
        """
    #Wind speed under cut_in value is changed to zero '0' assuming no wind so no energy generation.
    ws_limited = np.where(ws>cut_in, ws, 0)
    
    #Wind speed over cut_out value is changed to zero '0' assuming no wind so no energy generation.
    ws_limited = np.where(ws_limited<cut_out, ws_limited, 0)
    
    #Wind speed over rated_wind_speed value is fixed to wind speed value of rated_wind_speed.The maximum generation allowed 
    ws_limited = np.where(ws_limited<rated_wind_speed, ws_limited, rated_wind_speed) 
    return ws_limited

def calculating_density_height(u, v, tmp, prs=100367.63, cp=0.59, R=286.7):
    """ Returns new arranged DataArray of density at desired height (related to in which height the values are given)
    
        u  = u wind speed at any level (can be Xarray Datarray) m/s
        v  = v wind speed at any level (can be Xarray Datarray) m/s
        prs = pressure at any level,  to be dafult 80 metres is choosen --> 100367.63 Pa (can be Xarray Datarray)
        tmp = temperature at any level (can be Xarray Datarray) K
        cp = efficiency parameter
        R = Characteristic Gas Constant of air 286.7 J/kgK
        ws = wind speed at any level m/s 
        dense_height = The density that calculated with given values m3/kg
        
        IMPORTANT:cut_in, cut_out, rated_wind_speed, rated_power values are unique to the turbine used, can differ.
                    For Default Values "Vestas V82-1.5"  model is used.
        
        """
    
    u = u.values * units.meters / units.second
    v = v.values * units.meters / units.second
    ws = mpcalc.wind_speed(u, v)  # m/s
    ws = np.array(ws)
    dense_height = (prs / (R * tmp) ) 
    return np.array(dense_height)

def calculating_power_output(density, wind_speed, cp=0.59, swept_area=5281, rated_power=1.5):
    """ Returns Power with limited and arranged wind speed values.
    
        density  = density of the air m3/kg
        wind_speed  = wind speed at any level (can be Xarray Datarray) m/s
        cp = efficiency parameter
        swept area = the area that blades of turbine draws m2
        rated_power = Maximum power turbine generates corresponds to rated_wind_speed MW
        powers = the calculation of power with a basic formula MW
        power_limited = limiting power output under rated_power (max. capacity of the turbine)
        
        NOTE:Do the power output calculation after you are sure that the wind speed limitations are considered
                                        (cut_in, cut_out etc)
                                        
        IMPORTANT:cut_in, cut_out, rated_wind_speed, rated_power values are unique to the turbine used, can differ.
                    For Default Values "Vestas V82-1.5"  model is used.

        """
    #formula is used to calculate power
    powers =   ((0.5) * density * (wind_speed**3) * cp * swept_area) / (10**6)
    
    #limiting power output to below rated_power by assigning upper values to zero which indicates no power available
    power_limited = np.where(powers<=rated_power,powers, 0) 
    
    return power_limited

def uv_to_ws(u, v):
    """Return wind speed using u and v winds in m/s
    """
    u = u.values * units.meters / units.second
    v = v.values * units.meters / units.second
    ws = mpcalc.wind_speed(u, v)  # m/s
    ws = np.array(ws)
    return ws