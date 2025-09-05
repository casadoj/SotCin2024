#!/bin/bash

PATH_IN="./"
INPUT_FILE="${PATH_IN}/stations.txt"
PATH_OUT="${PATH_IN}/../cutmaps/masks/"
# PATH_OUT="/BGFS/DISASTER/casadje/GloFASv5/stations/South_America/catchstats/masks_1/"

# Check if the input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: $INPUT_FILE not found!"
    exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$PATH_OUT"

# Read the input file line by line
while IFS=$'\t' read -r longitude latitude id; do
    # Strip out carriage return characters
    id=$(echo "$id" | tr -d '\r')

    # Define source and destination paths
    src="${PATH_IN}/${id}/my_mask.nc"
    dest="${PATH_OUT}/${id}.nc"

    # Attempt to copy the file
    if [[ -f "$src" ]]; then
        cp "$src" "$dest"
        # echo "Copied: $src to $dest"
    else
        echo "ERROR: $id"
    fi
done < "$INPUT_FILE"

echo "Script completed."
