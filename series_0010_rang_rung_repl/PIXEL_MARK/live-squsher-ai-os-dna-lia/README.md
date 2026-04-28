Use

quckstart.sh

Or follow the steps below.

~~~
# Start
python3 ai_dna_main.py

# the above uses all the below
# ai_dna_squashfs.py
# ai_dna_chunksquash.py
# ai_dna_os.py
# ai_dna_os_fs.py

wait

echo Running ai_dna_chunker as a sub-process

# Wait
wait

echo Working... Chunks Created

# Wait
wait

# Start
bash ./copy_json.sh

# Wait
wait

# Start
bash ./copy_squash.sh

# Wait
wait

# Start
python3 hive_file_chunkerV2.py

# Wait
wait

# Start
# Uncoment to decode the JSON and have it included.
# This can can cause the final outputs to be large
# It is for doing inegrity checks on the processed files
# python3 hive_file_dechunkerV2.py

echo Skipping decoding step as intended...

# Wait
wait

# Start
python3 ai_dna_squashfs2.py

# Wait
wait

# Start
python3 ai_dna_chunksquash2.py

# Wait
wait

echo Working... Chunked Second Squashfs

# Start
bash ./create_html.sh

# Wait
wait

chromium %U --user-data-dir="~/chrome-dev-disabled-security" --disable-web-security --disable-site-isolation-trials --allow-file-access-from-files --allow-insecure-localhost ./start.html

# Start
echo Done!
~~~

OLDER VERSION OF README BELOW.

All required files are included in this repo.

The main entry point:

start.html


NOTES:

To chunk files located in the 'inputs' folder into JSON use:

hive_file_chunkerV2.py

This is not required but to test the integrity of the chunked files do:

hive_file_dechunkerV2.py

To create an html containing all chunked JSON files:

create_html.sh

The resulting JSON chunks are stored here:

chunky.html


The following javascript file is for handling blob urls:

blobHandler.js


This is used to handle gzip compression.

pako_inflate.min.js

It can be found here: https://unpkg.com/pako@0.2.7/dist/pako_inflate.min.js
