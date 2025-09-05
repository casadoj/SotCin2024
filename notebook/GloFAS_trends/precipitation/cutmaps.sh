#!/bin/bash

# set number of threads
export NUMEXPR_MAX_THREADS=$(nproc)

# activate Conda environment
source /BGFS/DISASTER/casadje/miniconda3/etc/profile.d/conda.sh
conda activate utils_new

# Define the path to the input file
LOC="south_america"
PATH_GLOFAS="/BGFS/COMMON/casadje/GloFAS4/static_maps/"
PATH_DATASET="/BGFS/DISASTER/casadje/GloFASv5/stations/${LOC}/cutmaps"
INPUT_FILE="${PATH_DATASET}/stations.txt"

# Check if the input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Error: File '$INPUT_FILE' not found."
  exit 1
fi

# Read the input file line by line
while IFS=$'\t' read -r longitude latitude id; do
  # Strip out carriage return characters
  id=$(echo "$id" | tr -d '\r')
  
  # Create a directory with the ID as the name
  path_station="${PATH_DATASET}/$id"
  mkdir -p "$path_station"

  # In the current directory, create a new text file with only the three values of the current point
  file_station="${path_station}/station.txt"
  echo -e "${longitude}\t${latitude}\t${id}" > "$file_station"

  # Execute the 'cutmaps' command with the appropriate arguments
  cutmaps -F "${PATH_GLOFAS}/upArea_repaired.nc" \
          -l "${PATH_GLOFAS}/ldd_repaired.map" \
          -N "$file_station" \
          -o "$path_station" \
          # -W

  # Clean up the 'station.txt' file for the next iteration
  rm "$file_station"
done < "$INPUT_FILE"
