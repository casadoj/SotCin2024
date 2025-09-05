# Precipitation trends in ERA5

This folder contains analysis of precipitation trends in the ERA5 forcings in GloFAS5, as they may affect its calibration.

Before running the notebooks, areal timeseries of precipitation have been created using the [`lisflood-utilities`](https://github.com/ec-jrc/lisflood-utilities) tools:

1. [`cutmaps`](https://github.com/ec-jrc/lisflood-utilities/wiki/cutmaps) to produce the catchment masks for each of the streamflow stations. A template of the Bash script is in this same folder ([`cutmaps.sh`](cutmaps.sh)).
2. [`catchstats`](https://github.com/ec-jrc/lisflood-utilities/wiki/catchstats) to compute the areal precipitation time series.A template of the Bash script is in this same folder ([`catchstats.sh`](catchstats.sh)).

## Cases

* [**Congo**](congo.ipynb)
* [**South America**](south_america.ipynb)