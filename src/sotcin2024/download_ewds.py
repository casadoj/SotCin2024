import cdsapi
from pathlib import Path
from tqdm import tqdm
import argparse
from datetime import datetime


# Set up argument parser
parser = argparse.ArgumentParser(description='Download GloFAS4 data from the Early Warning Data Store.')
parser.add_argument(
    '--path', type=str, required=True, help='Base path where the data will be saved.'
)
parser.add_argument(
    '--var', type=str, required=True, choices=['dis', 'rowe', 'swe', 'swi'],
    help=(
        "Variable to be downloaded: "
        "'dis':   river discharge in the last 24 hours (m3/s)"
        "'rowe':  runoff water equivalent (kg/m2)"
        "'swe':   snow water equivalent (kg/m2)"
        "'swi':   soil wetness index (-)"
    )
)
parser.add_argument(
    '--start', type=int, default=1979, help='Start year for data download.'
)
parser.add_argument(
    '--end', type=int, default=datetime.now().year - 1, help='End year for data download.'
)
args = parser.parse_args()

# Read arguments
PATH = Path(args.path)
VAR = args.var
START = args.start
END = args.end

# output path
path_var = PATH / VAR
path_var.mkdir(parents=True, exist_ok=True)

# Variables to download
variable_map = {
    'dis': 'river_discharge_in_the_last_24_hours',
    'rowe': 'runoff_water_equivalent',
    'swe': 'snow_depth_water_equivalent',
    'swi': 'soil_wetness_index'
}

# Initialize the client
client = cdsapi.Client(timeout=600)  # Increase timeout as needed

dataset = 'cems-glofas-historical'

# Loop through years and variables to download data
for year in tqdm(range(START, END + 1), desc='Year'):
        
    out_file = path_var / f'{VAR}_{year}.nc'
    if out_file.is_file():
        print(f'File {out_file} already exists, skipping.')
        continue
    request = {
        'system_version': ['version_4_0'],
        'hydrological_model': ['lisflood'],
        'product_type': ['consolidated'],
        'variable': [variable_map[VAR]],
        'hyear': [f'{year}'],
        'hmonth': [f'{month:02}' for month in range(1, 13)],
        'hday': [f'{day:02}' for day in range(1, 32)],
        'data_format': 'netcdf',
        'download_format': 'unarchived'
    }
    client.retrieve(dataset, request).download(out_file)
    print(f'Saved file: {out_file}')
