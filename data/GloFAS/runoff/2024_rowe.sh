#!/bin/bash

source activate pyg2p_env || conda activate pyg2p_env

VAR='rowe'

# cd PATH_USER
python E:/casadje/GitHub/SotCin2024/src/sotcin2024/long_term_average.py -i "Z:/nahaUsers/casadje/GloFASv4/long_run/${VAR}" -v "${VAR}" -s 2024-01-01 -e 2024-12-31
