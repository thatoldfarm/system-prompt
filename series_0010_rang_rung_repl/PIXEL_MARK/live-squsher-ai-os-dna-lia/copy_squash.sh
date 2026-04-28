#!/bin/bash

# Define the directory where the files are to be copied
destination_folder="inputs"

# Check if the destination folder exists, if not, create it
if [ ! -d "$destination_folder" ]; then
    mkdir "$destination_folder"
fi

# Copy the specified JSON files to the destination folder
cp outputs2.squashfs "$destination_folder/"
cp outputs.squashfs "$destination_folder/"

echo "Files copied to $destination_folder"
