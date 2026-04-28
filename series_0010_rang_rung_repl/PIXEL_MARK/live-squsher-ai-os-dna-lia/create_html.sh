#!/bin/bash

# Directory containing the JSON chunks
chunks_dir="outputs/chunks"

# The HTML file to be created
output_html="chunky.html"

# Start the HTML file with some basic structure
echo '<!DOCTYPE html>' > $output_html
echo '<html><head><title>Chunky</title></head><body>' >> $output_html
echo '<script>' >> $output_html
echo 'let data = "";' >> $output_html

# Sort files and concatenate their contents into the HTML file
for file in $(ls $chunks_dir | sort -V); do
    # Extract the base filename or file identifier
    file_identifier=$(echo $file | sed 's/_chunks_chunk[0-9]*\.json//')

    # Start JSON object
    echo "data += \`{\"file\": \"$file_identifier\", \"content\": " >> $output_html
    
    # Add actual JSON content
    cat "$chunks_dir/$file" >> $output_html

    # Close JSON object
    echo "}\`;" >> $output_html
done

# Close the script and HTML tags
echo '</script>' >> $output_html
echo '</body></html>' >> $output_html

echo "Chunky.html has been created with embedded JSON data."
