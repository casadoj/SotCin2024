from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.stats import linregress
import matplotlib as mpl
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def compute_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Computes the linear trend of a set of annual time series
    
    Attributes:
    -----------
    df: pandas.DataFrame
        Time series fro which the trend will be computed. Columns represent stations/
        catchments, rows represent time steps

    Returns:
    --------
    pandas.DataFrame:
        Slope, intercept and p-value of the linear trend of each of the input time series   
    """
    trends = {}
    for ID in df.columns:
        slope, intercept, r_value, p_value, std_err = linregress(df.index, df[ID])
        trends[ID] = {
            'slope': slope,
            'intercept': intercept,
            'pval': p_value
        }
    return pd.DataFrame(trends)


def create_cmap(
    cmap: str,
    bounds: List,
    name: str = '',
    specify_color: Tuple = None
):
    """Given the name of a colour map and the boundaries, it creates a discrete colour ramp for future plots
    
    Inputs:
    ------
    cmap:          string. Matplotlib's name of a colourmap. E.g. 'coolwarm', 'Blues'...
    bounds:        list. Values that define the limits of the discrete colour ramp
    name:          string. Optional. Name given to the colour ramp
    specify_color: tuple (position, color). It defines a specific color for a specific position in the colour scale. Position must be an integer, and color must be either a colour name or a tuple of 4 floats (red, gren, blue, transparency)
    
    Outputs:
    --------
    cmap:   List of colours
    norm:   List of boundaries
    """
    
    cmap = plt.get_cmap(cmap)
    cmaplist = [cmap(i) for i in range(cmap.N)]
    if specify_color is not None:
        cmaplist[specify_color[0]] = specify_color[1]
    cmap = mpl.colors.LinearSegmentedColormap.from_list(name, cmaplist, cmap.N)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    return cmap, norm


def map_stations(
    stations: gpd.GeoDataFrame,
    s: Optional[Union[pd.Series, int]] = None,
    c: Optional[Union[pd.Series, str]] = None,
    **kwargs
):
    """
    """

    # Keyword arguments
    figsize = kwargs.get('figsize', (8, 8))
    proj = kwargs.get('proj', ccrs.PlateCarree())
    extent = kwargs.get('extent', [-180, 180, -60, 90])
    cmap_name = kwargs.get('cmap', 'coolwarm_r')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': proj})
    
    # Set extent to South America [west, east, south, north]
    ax.set_extent(extent, crs=proj)
    
    # Add background features
    ax.add_feature(cfeature.LAND, facecolor='whitesmoke', zorder=0)
    ax.add_feature(cfeature.RIVERS, edgecolor='steelblue', zorder=1)
    
    s = 6 if s is None else s
    c = 'dimgrey' if c is None else c
    if isinstance(c, pd.Series):
        cmap, norm = create_cmap(cmap_name, np.arange(-10, 11, 1))
    else:
        cmap, norm = None, None
    ax.scatter(
        stations.geometry.x, 
        stations.geometry.y, 
        s=s, 
        c=c, 
        cmap=cmap,
        norm=norm,
        alpha=.75,
        zorder=2
    )

    if 'title' in kwargs:
        ax.set_title(kwargs['title'])
    if isinstance(c, pd.Series):
        cbar = plt.colorbar(
            ScalarMappable(norm=norm, cmap=cmap), 
            ax=ax, 
            orientation='vertical', 
            shrink=0.5, 
            pad=0.05
        )
        if 'label' in kwargs:
            cbar.set_label(kwargs['label'])
    
    ax.axis('off');