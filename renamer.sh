#!/bin/bash

# Loop through all folders
for folder in *_assignsubmission_file; do
    # Extract $DAY and $GROUPID
    DAY=$(echo "$folder" | awk -F'[()]' '{print $2}')
    GROUPID=$(echo "$folder" | awk -F'groupe ' '{split($2, a, "_"); print a[1]}')
    
    # Form the new name
    new_name="${DAY}_${GROUPID}"
    
    # Rename the folder
    mv "$folder" "$new_name"
    echo "Renamed: '$folder' -> '$new_name'"
done

