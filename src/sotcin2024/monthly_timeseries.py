import pandas as pd
import xarray as xr
from pathlib import Path
import argparse
from datetime import datetime

# Set up argument parser
parser = argparse.ArgumentParser(
    description='Compute the monthly time series global average.'
)
parser.add_argument(
    '-i',
    '--input',
    type=str,
    required=True,
    help='Path where the input NetCDF files are saved.'
)
parser.add_argument(
    '-v',
    '--var',
    type=str,
    default='rowe',
    choices=['dis24', 'rowe', 'sd', 'swir'],
    help=(
        "Variable to be analysed: "
        "'dis24':   river discharge in the last 24 hours (m3/s)"
        "'rowe':  runoff water equivalent (kg/m2)"
        "'sd':   snow depth water equivalent (kg/m2)"
        "'swir':   soil wetness index (-)"
    )
)
parser.add_argument(
    '-s',
    '--start',
    type=str,
    default='1979-01-01',
    help='Start date (format: YYYY-MM-DD).'
)
parser.add_argument(
    '-e',
    '--end',
    type=str,
    default='2024-12-31',
    help='End date (format: YYYY-MM-DD).'
)
args = parser.parse_args()

# Read arguments
PATH = Path(args.input)
VAR = args.var
try:
    START = datetime.strptime(args.start, '%Y-%m-%d')
    END = datetime.strptime(args.end, '%Y-%m-%d')
except ValueError as e:
    raise ValueError(f"Invalid date format: {END}. Please use 'YYYY-MM-DD'.")

# output directory and output file
output_dir = PATH / 'thresholds'
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f'{VAR}_montly_mean_{START.year}-{END.year}.nc'

# list of input NetCDF files
files = sorted(PATH.glob(f'{VAR}_*.nc'))
files = [file for file in files if START.year <= int(file.stem.split('_')[1]) <= END.year]
if not files:
    raise FileNotFoundError(f"No files found in {PATH} matching pattern '{VAR}_*.nc'.")

# open dataset and crop to the study period
ds = xr.open_mfdataset(
    files,
    engine='netcdf4',
    chunks='auto',
)[VAR]

# rename variables
ds = ds.rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})

# convert time convention to beginning-of-timestep
ds['time'] = ds['time'] - pd.Timedelta(days=1)

# crop to the study period
ds = ds.sel(time=slice(START, END))

# monthly resample
ds_monthly = ds.resample(time='1M').mean(skipna=True)

# rechunk
ds_monthly = ds_monthly.chunk({'time': 1, 'lat':'auto', 'lon': 'auto'})

# compute global average
serie = ds_monthly.mean(['lat', 'lon'], skipna=True).compute()

# save output file
serie.to_netcdf(output_file)
print(f'Monthly time series of average global {VAR} saved in: {output_file}')