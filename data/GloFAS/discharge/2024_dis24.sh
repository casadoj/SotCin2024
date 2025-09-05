#!/bin/bash

source activate pyg2p_env || conda activate pyg2p_env

# VAR="$1"
# if [ -z "$VAR" ]; then
	# echo "Error: VAR is not provided. Usage: ./long_term_average.sh VAR"
	# exit 1
# fi

VAR='dis24'
PATH_USER='/BGFS/DISASTER/casadje'

# cd "${PATH_USER}/GitHub/SotCin2024/src/sotcin2024" || {
  # echo "Directory not found: ${PATH_USER}/GitHub/SotCin2024/src/sotcin2024"
  # exit 1
# }

# cd PATH_USER
python "${PATH_USER}/GitHub/SotCin2024/src/sotcin2024/long_term_average.py" -i "${PATH_USER}/GloFASv4/long_run/${VAR}" -v "${VAR}" -s 2024-01-01 -e 2024-12-31
