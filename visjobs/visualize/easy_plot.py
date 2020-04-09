# -*- coding: utf-8 -*-
"""

@author: Kutay
"""

#!/usr/bin/env python
# coding: utf-8
import warnings
warnings.filterwarnings("ignore")
import xarray as xr
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import cartopy
import numpy as np
import matplotlib as mpl
import scipy.ndimage as ndimage
import matplotlib.colors as mcolors
from netCDF4 import num2date
from matplotlib.animation import ArtistAnimation
import numpy as np
import matplotlib.animation as animation
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER , LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable

#make class for visualizing
class painter():
    
    def __init__(self):
        self=self
    
    def paint_ax(self, i=1, j=1, k=1, check_proj = False, proj='Mercator' ):
        """returning user a figure and axis with given parameters
           If projection will be used spot check_proj=True:
                                                   and define a projection
        """
        #availale cartopy projections
        proj_dict ={'Mercator':cartopy.crs.Mercator(),
                    'PlateCarree':cartopy.crs.PlateCarree()}
        fig = plt.figure()
        #check if proj is expected
        if check_proj == True:
            ax = fig.add_subplot(i, j, k, projection = proj_dict[proj])
        else:
            ax = fig.add_subplot(i, j, k,)
            
        self.ax = ax
        return self.ax
    #lets define the border feature using cartopy
    def paint_borders(self, ax=None , linewidths = 0.4, res='50m', **kwargs):
        """returns axis with borders from cartopy"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        borders = ax.add_feature(cartopy.feature.BORDERS.with_scale(res) , linewidths = linewidths, **kwargs)
        return borders
    
        
    
    #lets define the coastline feature using cartopy
    def paint_coastline(self, ax=None, linewidths = 0.6, res='50m', **kwargs):
        """returns axis with coastlines from cartopy"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        coasts = ax.add_feature(cartopy.feature.COASTLINE.with_scale(res) , linewidths = linewidths, **kwargs)
        return coasts
    
    #lets define the Land feature using cartopy
    def paint_land(self, ax=None, facecolor='lightgrey', res='50m', **kwargs):
        """returns axis with land from cartopy"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        lands = ax.add_feature(cartopy.feature.COASTLINE.with_scale(res) , facecolor = facecolor, **kwargs)
        return lands
    #let's define the ocean feature using cartopy
    def paint_ocean(self, ax=None, linewidths = 0.4, facecolor='lightblue', res='50m', **kwargs):
        """returns axis with land from cartopy"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        oceans = ax.add_feature(cartopy.feature.COASTLINE.with_scale(res), facecolor = facecolor, linewidths = linewidths, **kwargs)
        return oceans
        
    #let's define the states feature using cartopy
    def paint_states(self, ax=None, linewidths = 0.4, res='50m', **kwargs):
        """returns axis with states from cartopy"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        states = ax.add_feature(cartopy.feature.STATES.with_scale(res) , linewidths = linewidths, **kwargs)
        return states
    
    #let's define our extent 
    def paint_extent(self, ax=None, lon_lat=[], **kwargs):
        """return axis with set extent
           lon_lat should be given a list of lon and lat respectively
           lon_lat = [east,west,south,north]
           
           to make this easier for user paint_area function can be used
        """
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        extents = ax.set_extent(lon_lat)
        return extents

    #let's define the easily accesible extent areas
    def paint_area(self, area, ax=None):
        """returns the desired area of interest with set_extent"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        p_d = {'europe' : [0, 48, 30, 60],
              'northamerica' : [218,318,-10,70],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [260,285,14,37],
              'carribeans' : [275,300,12,38], 
              'indianocean' : [30, 130,-35,35]}
        #set the extent
        extents = ax.set_extent(p_d[area])
        return extents
    
    #let's define a setter for a size of the figure
    def set_size(self, a, b, ax=None ):
        """returns the changed figsize according to a and b values"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
            
        #let's set the figsize
        size = plt.rcParams['figure.figsize'] = a, b
        return size
    
    #let's set arrange for our will be plottings
    def set_arange(self, init, finit, interval, method='arange', **kwargs):
        """returns user either an numpy array using arange function or
           using linspace function.
           For further info  visit numpy package website
           #avaliable methods:
                    methods = {'arange':np.arange,
                               'linspace':np.linspace}
        """
        #avaliable methods
        methods = {'arange':np.arange,
                   'linspace':np.linspace}
        
        arng = methods[method](init, finit, interval, **kwargs)
        return arng
    
    #let's set the gridlines
    def set_gridlines(self,ax=None):
        """returns user a gridline"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        return ax.gridlines()
    
    #let's set lon and lat visible on the map
    def set_lonlat(self, ax=None, sizing=15, *args, **kwargs):
        """makes the longitude and latitude visible on the dges of the map"""
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
    
        gl = ax.gridlines(crs=cartopy.crs.PlateCarree(), draw_labels=True , *args, **kwargs)
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlabel_style = {'size': sizing,}
        gl.ylabel_style = {'size': sizing}

        return gl
    
    #let's define a contourplot
    def plot_contour(self, lon, lat, data, *args, transform='None', ax=None, **kwargs ):
        """returns contourplot of matplotlibs
           transform must be given string"""
        #available projections
        proj_dict ={'Mercator':cartopy.crs.Mercator(),
                    'PlateCarree':cartopy.crs.PlateCarree(),
                    'None':None}
        
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
        #get mesh
        mesh = ax.contour(lon, lat, data, *args, **kwargs, transform=proj_dict[transform])
        
        return mesh
    
    #let's define contourf plot
    def plot_contourf(self, lon, lat, data, *args, transform='None', ax=None, **kwargs ):
        """returns contourf of matplotlibs
           transform must be given string"""
        
        
        #available projections
        proj_dict ={'Mercator':cartopy.crs.Mercator(),
                    'PlateCarree':cartopy.crs.PlateCarree(),
                    'None':None}
            
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
        #get mesh
        mesh = ax.contourf(lon, lat, data, *args, **kwargs, transform=proj_dict[transform])
        return mesh
    
    #let's define pcolormesh plot
    def plot_pmesh(self, lon, lat, data, *args, transform='None', ax=None, **kwargs):
        """returns pcolormesh of matplotlibs
           transform must be given string """
        
        #available projections
        proj_dict ={'Mercator':cartopy.crs.Mercator(),
                    'PlateCarree':cartopy.crs.PlateCarree(),
                    'None':None}
        
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
        #get mesh
        mesh = ax.pcolormesh(lon, lat, data, *args, **kwargs, transform=proj_dict[transform])
        return mesh
    
    #let's define colorbar ### COLORBAR FUNCTION IS DERIVED FROM TOMER BURG GITHUB.COM/TOMERBURG ###
    def plot_colorbar(self,mappable=None,location='right',size="3%",pad='1%', sizing=15,fig=None,ax=None,**kwargs):
        """
        Uses the axes_grid toolkit to add a colorbar to the parent axis and rescale its size to match
        that of the parent axis, similarly to Basemap's functionality.
        
        Parameters:
        ----------------------
        mappable
            The image mappable to which the colorbar applies. If none specified, matplotlib.pyplot.gci() is
            used to retrieve the latest mappable.
        location
            Location in which to place the colorbar ('right','left','top','bottom'). Default is right.
        size
            Size of the colorbar. Default is 3%.
        pad
            Pad of colorbar from axis. Default is 1%.
        ax
            Axes instance to associated the colorbar with. If none provided, or if no
            axis is associated with the instance of Map, then plt.gca() is used.
        """
        
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
        #Get current mappable if none is specified
        if fig is None or mappable is None:
            import matplotlib.pyplot as plt
        if fig is None:
            fig = plt.gcf()
            
        if mappable is None:
            mappable = plt.gci()
        
        #Create axis to insert colorbar in
        divider = make_axes_locatable(ax)
        
        if location == "left":
            orientation = 'vertical'
            ax_cb = divider.new_horizontal(size, pad, pack_start=True, axes_class=plt.Axes)
        elif location == "right":
            orientation = 'vertical'
            ax_cb = divider.new_horizontal(size, pad, pack_start=False, axes_class=plt.Axes)
        elif location == "bottom":
            orientation = 'horizontal'
            ax_cb = divider.new_vertical(size, pad, pack_start=True, axes_class=plt.Axes)
        elif location == "top":
            orientation = 'horizontal'
            ax_cb = divider.new_vertical(size, pad, pack_start=False, axes_class=plt.Axes)
        else:
            raise ValueError('Improper location entered')
        
        #Create colorbar
        fig.add_axes(ax_cb)
        cb = plt.colorbar(mappable, orientation=orientation, cax=ax_cb, **kwargs)
        cb.ax.tick_params(labelsize=sizing)
        
    #let's define the clabel of the contourplot
    def plot_clabel(self, mesh, fontsize=18, *args, ax=None, **kwargs ):
        """returns clabel of contourplot of matplotlibs
           """
        #available projections
        proj_dict ={'Mercator':cartopy.crs.Mercator(),
                    'PlateCarree':cartopy.crs.PlateCarree(),
                    'None':None}
        
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
        #get clabel
        mesh2 = ax.clabel(mesh, fontsize=fontsize, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , )
        return mesh2
    
    #let's define title
    def set_title(self, title, up=1.02, right=0,  *args, fontsize=12,  ax=None, **kwargs):
        """
        returns title
        title must be given string
        """
        
        #check if axis exists
        if ax == None:
            ax = self.paint_ax(check_proj=True, proj='Mercator')
        
            
        titles = ax.text(right, up, title,  fontsize=fontsize,  **kwargs)
        return titles