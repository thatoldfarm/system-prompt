#!/bin/bash

# Set the maximum number of characters per file
max_chars=43000

# Read the input file
input=$(<input.txt)

# Initialize variables for the loop
file_number=0
chunk=""

# Loop through each character in the input
for (( i=0; i<${#input}; i++ )); do
    # Get the current character
    char=${input:$i:1}

    # Add the character to the current chunk
    chunk+=$char

    # If the chunk has reached the maximum number of characters, write it to a new file and reset the chunk
    if [[ ${#chunk} -ge $max_chars ]]; then
        file_number=$((file_number + 1))
        echo "$chunk" > "output_$file_number.txt"
        chunk=""
    fi
done

# Write any remaining characters in the chunk to the final output file
echo "$chunk" > "output_$((file_number + 1)).txt"

