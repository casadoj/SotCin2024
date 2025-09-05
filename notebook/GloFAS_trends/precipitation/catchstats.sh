#!/bin/bash

# set number of threads
export NUMEXPR_MAX_THREADS=$(nproc)

# activate Conda environment
source /BGFS/DISASTER/casadje/miniconda3/etc/profile.d/conda.sh
conda activate utils_new

# paths
VAR="tp"
LOC="south_america"
PATH_METEO="/BGFS/DISASTER/casadje/GloFASv5/meteo/${VAR}/${LOC}/"
PATH_DATASET="/BGFS/DISASTER/casadje/GloFASv5/stations/${LOC}/catchstats"
MAP_PIXAREA="/BGFS/DISASTER/casadje/GloFASv5/static_maps/pixarea_Global_03min.nc"

# create output directory
path_out="${PATH_DATASET}/${VAR}"
mkdir -p "$path_out"

# run the tool
catchstats -i "$PATH_METEO" \
           -m "${PATH_DATASET}/../cutmaps/masks/" \
           -s mean \
           -o "$path_out" \
           -a "$MAP_PIXAREA"
