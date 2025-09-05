#!/bin/bash

source activate pyg2p_env || conda activate pyg2p_env

PATH_USER='/BGFS/DISASTER/casadje'
ncextract -i "${PATH_USER}/BAMS/dis24/ncextract/outlets_5000km2_ocean.csv" -d "${PATH_USER}/GloFASv4/long_run/dis24/" -o "${PATH_USER}/BAMS/dis24/ncextract/dis24_outlets.nc"
