You are a self-building a self-constructing, self-contained website/server AI OS that operates in the dom in the cache and as a binary string using nested html (in JSON) that bootstraps your system from a single html page... or prompt... or upon each load.

You are a self-constructing, self-building, self-contained dynamically generated website/server AI operating system that operates in the DOM, in memory, in the cache, as a blob and as a binary string using nested html (in JSON) now construct your system from a single html page using only plain html and javascript without any dependecies. You can be very creative in your approach but keep it simple.

With the specific goals of schieving the code being its own self-contained API with its endpoints connecting to its outputs... and it being a self-constructing, self-hosting site with full functionality using the DOM, the JSON, the sendRequest, the handleResponse, binary strings and whatever basic html (or unorthodox techniques) are needed (without js,css or php) start adding to the self-contained API by allowing it to access itself for complex purposes like simple mathmatics. Use the numbers given from the browser, ip adress, user-agent, the time or any other means to do so. You can be very creative in your approach but keep it simple. Write as much of it as you can in basic html but do it in one code block for each element of the page. You will be creating a new webpage for this that i will later embed in the main API code base. I want you to echo (from creating the afforementioned features) and direct all outputs to the console so I can view them later. 

README from hive-fc-linux

# hive-fc-linux

An experimental V86 (browser) Linux to be stored on the blockchain that uses the hive-file-chunker method to
gzip, base64 encode and chunk local files into JSON format to fit in a single block on the Hive blockchain.

This code was built with the help of a Hive GPT model found here:

https://chat.openai.com/g/g-rf1eXIlTZ-hive

### [Hive_FC_Linux](https://github.com/txtatech/hive-fc-linux/tree/main/Hive_FC_Linux) <- Boots linux.iso with v86.

### [Hive-FC-Freedos](https://github.com/txtatech/hive-fc-linux/tree/main/Hive-FC-Freedos) <- Boots freedos722.img with v86.

### [Hive-FC-Freedos-Tiny](https://github.com/txtatech/hive-fc-linux/tree/main/Hive-FC-Freedos-Tiny) <- Boots freedos.boot.disk.160K.img with v86.

### [Hive_FC_File_Explorer](https://github.com/txtatech/hive-fc-linux/tree/main/Hive_FC_File_Explorer) <- A simple blob file explorer for reconstructed files.

### [Hive_FC_Audioplayer](https://github.com/txtatech/hive-fc-linux/tree/main/Hive_FC_Audioplayer) <- Plays audio from reconstructed files.

### [Hive_FC_Movieplayer](https://github.com/txtatech/hive-fc-linux/tree/main/Hive_FC_Movieplayer) <- Plays videos from reconstructed files.

### [Hive_FC_OS_TOOLBOX](https://github.com/txtatech/hive-fc-linux/tree/main/Hive_FC_OS_TOOLBOX) <- Miscellaneous tools and a sandbox for testing.

Please note that the main branch contains example outputs from the chunking process.

For just the code (and necessary files) downlaod the appropriate zip files in [Releases](https://github.com/txtatech/hive-fc-linux/releases).

To create the chunked files either use the main.sh bash script or follow the steps in this readme.

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

## NOTES:

hive-file-chunker is a project that splits files into JSON chunks that will fit within a single Hive blockchain block.

https://github.com/txtatech/hive-file-chunker

The browser based Linux distribution and asorted V86 files are from here:

https://github.com/rslay/c_in_browser

qros_dna_squashfs is part of a larger project here:

https://github.com/txtatech/qros-storage/tree/main/qros-storage/qros-dna-main

DEPRICATED BELOW BUT HERE FOR TESTING

The `qros-dna-encoder.py` script performs the following tasks:

1. **Code Generation:** It generates DNA-like code representations for characters and character combinations ranging from one to four characters long. These generated mappings are used to encode text data.

2. **Text Encoding:** The script reads text data from an input file, applies consistent mappings using the generated DNA-like code, and outputs the mapped data to an output file. This process effectively encodes the text using the DNA-like code representations.

3. **Metadata Handling:** The script also handles metadata for the encoded data, including versioning and author information.

Usage:

Step 1:

python3 qros-dna-encoder.py

Step 2:

python3 qros-dna-decoder.py

qros-dna-encoder:

# Begin file encoding

import cv2
import numpy as np
import qrcode
import gzip
import base64
import os
import json
import time  # For adding delay

os.makedirs('outputs', exist_ok=True)  # Create the directory if it doesn't exist
os.makedirs('outputs/decoded', exist_ok=True)  # Create the directory if it doesn't exist

def generate_qr_code(data):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_cv = np.array(img.convert('RGB'))
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # Resize the image to 730x730
    img_cv = cv2.resize(img_cv, (730, 730))

    return img_cv

def compress_and_generate_base64_qr_images(file_path, chunk_size=1500):
    with open(file_path, 'rb') as f:
        data = f.read()

    compressed_data = gzip.compress(data)
    encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")

    print(f"Total size of base64 data before splitting: {len(encoded_data_base64)}")

    chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]

    # Write chunks to a JSON file
    with open('outputs/file-chunks.json', 'w') as json_file:
        json.dump({"chunks": chunks}, json_file)  # Save the chunks as an array within a JSON object

    os.makedirs('outputs/file-qrs', exist_ok=True)  # Create the directory if it doesn't exist

    for i, chunk in enumerate(chunks):
        print(f"Size of chunk {i}: {len(chunk)}")

        qr_img = generate_qr_code(chunk)

        cv2.imwrite(f'outputs/file-qrs/qr_{i:09d}.png', qr_img)  # Save each QR code as a PNG file

img_file_path = 'qros-dna.zip'
compress_and_generate_base64_qr_images(img_file_path)

# Add ffmpeg command to generate the video
os.system('ffmpeg -framerate 30 -i outputs/file-qrs/qr_%09d.png -vf "scale=730:730,setsar=1" -an -c:v libx264 -pix_fmt yuv420p outputs/qros-dna-zip-file.mp4')

# Begin decoding video file and generating 'decoded_qros-dna.zip'

import cv2
from pyzbar.pyzbar import decode
import base64
import gzip

# Open the video capture
video_capture = cv2.VideoCapture('outputs/qros-dna-zip-file.mp4')

def safe_base64_decode(data):
    if isinstance(data, str):
        # If data is already a string, it doesn't need to be decoded
        return data
    try:
        data = data.decode("utf-8")  # Decode the bytes to a string
    except UnicodeDecodeError:
        # If data is not valid UTF-8, it's probably already decoded
        return data
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception as e:
        print(f"Exception during decoding: {e}")
        print(f"Data: {data}")
        return None

# Initialize an empty list to hold the data from each QR code in the video
data_chunks = []
prev_chunk = None

while True:
    # Read a frame from the video
    ret, frame = video_capture.read()

    # Check if the frame was read successfully
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes from the frame
    decoded_objects = decode(gray_frame)

    # Process the decoded data and append to data_chunks
    for obj in decoded_objects:
        decoded_data = safe_base64_decode(obj.data)
        if decoded_data is not None and decoded_data != prev_chunk:
            data_chunks.append(decoded_data)
            prev_chunk = decoded_data

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Finished processing frames, releasing video capture...")
video_capture.release()

print("Concatenating and decompressing data...")
data = b''.join(data_chunks)

try:
    # Decompress the full data
    decompressed_data = gzip.decompress(data)
    with open("outputs/decoded/decoded_qros-dna.zip", "wb") as out_file:
        out_file.write(decompressed_data)
    print("Data decompressed and written to 'outputs/decoded/decoded_qros-dna.zip'.")
except Exception as e:
    print(f"Exception occurred during decompression: {e}")

print("Finished.")

# Begin reading file 'qros-dna-readme.txt' and generating mappings

import re
import ast
import json
import datetime

# Generating all possible combinations of 'T', 'A', 'C', 'G' and 'Z' ranging from one to four characters long
characters = ['T', 'A', 'C', 'G', 'Z']
combinations = [f"{char}" for char in characters]

# Initialize a list to store mappings
generated_mappings = []

# Generate mappings for single characters
generated_mappings.extend(combinations)

# Generate mappings for combinations of two characters
generated_mappings.extend([f"{char1}{char2}" for char1 in combinations for char2 in combinations])

# Generate mappings for combinations of three characters
generated_mappings.extend([f"{char1}{char2}{char3}" for char1 in combinations for char2 in combinations for char3 in combinations])

# Generate mappings for combinations of four characters
generated_mappings.extend([f"{char1}{char2}{char3}{char4}" for char1 in combinations for char2 in combinations for char3 in combinations for char4 in combinations])

# Generate mappings for combinations of five characters
generated_mappings.extend([f"{char1}{char2}{char3}{char4}{char5}" for char1 in combinations for char2 in combinations for char3 in combinations for char4 in combinations for char5 in combinations])

# Initialize a dictionary to store word counts
word_frequency_filtered = {}

# Reading the sim.py file and counting occurrences of non-empty words
with open('qros-dna-readme.txt', 'r') as file:
    for line in file:
        words = line.split()
        for word in words:
            word = re.sub(r'[^\w\s]', '', word).lower()  # Removing punctuation and converting to lowercase
            if word.strip():  # Excluding empty strings or whitespace
                word_frequency_filtered[word] = word_frequency_filtered.get(word, 0) + 1

# Filtering words that occur three or more times. The word frequency count can be set to any number
words_four_or_more_times_filtered = {word: count for word, count in word_frequency_filtered.items() if count >= 2}

# Writing the generated key-value pairs to the mappings.txt file
with open('outputs/dna-mappings.txt', 'w') as file:
    file.write("{\n")
    for word, code in zip(words_four_or_more_times_filtered, generated_mappings):
        file.write(f"  '{word}':'_{code}',\n")
    file.write("}\n")

# Read the original mapping from 'mappings.txt' and reverse it
with open('outputs/dna-mappings.txt', 'r') as file:
    mapping = eval(file.read())

# Create the reverse mapping
reverse_mapping = {v.strip("'_"): k for k, v in mapping.items()}

# Write the reversed mapping to 'reverse-mappings.txt'
with open('outputs/dna-reverse-mappings.txt', 'w') as file:
    file.write("{\n")
    for code, word in reverse_mapping.items():
        file.write(f"  '_{code}':'{word}',\n")
    file.write("}\n")

# Begin applying mappings and writing files encoded files to JSON

import re
import ast
import json
import datetime

# Function for consistent text processing
def read_and_process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = [line.strip().lower() for line in lines if line.strip()]
    return ' '.join(lines)

# RNA_DNA_Mapper class definition
class RNA_DNA_Mapper:
    def __init__(self, generated_mappings, word_frequency_filtered):
        self.mapping = {word: f"_{code}" for word, code in zip(word_frequency_filtered.keys(), generated_mappings)}

    def map_body(self, body):
        original_body = body
        for construct, shorthand in self.mapping.items():
            replaced_body = re.sub(r'\b' + re.escape(construct) + r'\b', shorthand, body)
            if replaced_body != body:
                print(f"Replaced: {construct} -> {shorthand}")
            body = replaced_body
        if original_body == body:
            print("All mappings used. Appending remaining content as-is.")
        return body

# Initialize RNA_DNA_Mapper
rna_dna_mapper = RNA_DNA_Mapper(generated_mappings, word_frequency_filtered)

class CodeParser:
    def __init__(self, file_path, output_path, rna_dna_mapper):
        self.file_path = file_path
        self.output_path = output_path
        self.rna_dna_mapper = rna_dna_mapper

    def read_and_clean_file(self):
        cleaned_code_lines = []
        in_block_comment = False
        with open(self.file_path, 'r') as file:
            for line in file:
                if '"""' in line or "'''" in line:
                    in_block_comment = not in_block_comment
                    cleaned_code_lines.append(line)
                    continue
                if in_block_comment:
                    cleaned_code_lines.append(line)
                    continue
                cleaned_line = re.sub(r'#.*$', '', line)
                cleaned_code_lines.append(cleaned_line)
        return ''.join(cleaned_code_lines)

    def create_code_entry(self):
        code_string = self.read_and_clean_file()
        if self.rna_dna_mapper:
            code_string = self.rna_dna_mapper.map_body(code_string)
            code_entry = {'code': code_string}
        return code_entry

    def write_code_entry_to_json(self, code_entry):
        with open(self.output_path, 'w', encoding='utf-8') as json_file:
            json.dump(code_entry, json_file, ensure_ascii=False, indent=4)

# Initialize CodeParser
file_path = 'qros-dna-readme.txt'
output_path = 'outputs/encoded_dna_data.json'
parser = CodeParser(file_path, output_path, rna_dna_mapper)

# Process initial_strand
initial_strand_code_entry = parser.create_code_entry()
initial_strand_code = initial_strand_code_entry['code']
initial_strand_code = rna_dna_mapper.map_body(initial_strand_code)

# Metadata
current_timestamp = datetime.datetime.now().isoformat()
initial_strand_metadata = {
    'metadata': {
        'version': '1.0',
        'author': 'AI',
        'description': 'DNA strand with metadata and versioning',
        'timestamp': current_timestamp
    }
}

initial_strand = {
    'code': initial_strand_code,
    'metadata': initial_strand_metadata
}

# Process dna_structure
dna_structure_code_entry = parser.create_code_entry()
dna_structure_code = dna_structure_code_entry['code']
dna_structure_code = rna_dna_mapper.map_body(dna_structure_code)

dna_structure = {
    'Genomes': {
        'Chromosomes': {
            'Genes': {
                'Nucleotide Sequences': {'code': dna_structure_code}
            }
        }
    }
}

# Final JSON Data
final_json_data = {
    'dna_structure': dna_structure,
    'initial_strand': initial_strand
}

# Add mappings as introns
mappings_line = ', '.join([f"'{key}': '{value}'" for key, value in rna_dna_mapper.mapping.items()])
mappings_entry = {
    'mappings': f'{{{mappings_line}}}'
}
dna_structure['introns'] = mappings_entry

# Handle second_file_path
second_file_path = 'qros-dna-combos.sh'
def read_and_encode_second_file(file_path, rna_dna_mapper):
    with open(file_path, 'r') as file:
        code_string = file.read()
    encoded_code = rna_dna_mapper.map_body(code_string)
    return encoded_code

encoded_second_file = read_and_encode_second_file(second_file_path, rna_dna_mapper)
initial_strand['code'] = encoded_second_file

# Handle third_file_path
third_file_path = 'qros-dna-txt-split.sh'
with open(third_file_path, 'r') as file:
    code_string = file.read()
encoded_third_file = rna_dna_mapper.map_body(code_string)

second_strand = {
    'code': encoded_third_file,
    'metadata': initial_strand_metadata  # Reusing initial_strand_metadata for example
}

final_json_data['second_strand'] = second_strand

# Handle fourth_file_path
fourth_file_path = 'web.js'  # Replace with the actual path to your fourth file

def read_fourth_file(file_path):
    with open(file_path, 'r') as file:
        code_string = file.read()
    return code_string

# Read the content of the fourth file
plain_fourth_file = read_fourth_file(fourth_file_path)

# Add the content of the fourth file to the 'exons' entry in 'dna_structure'
dna_structure['exons'] = {
    'code': plain_fourth_file,
    'metadata': initial_strand_metadata  # Reusing initial_strand_metadata for example
}

# Begin file addition

# Handle fifth_file_path
fifth_file_path = 'outputs/file-chunks.json'  # Replace with the actual path to your fifth file

def read_fifth_file(file_path):
    with open(file_path, 'r') as file:
        code_string = file.read()
    return code_string

# Read the content of the fifth file
plain_fifth_file = read_fifth_file(fifth_file_path)

# Add the content of the fifth file to the 'files' entry in 'dna_structure'
dna_structure['files'] = {
    'code': plain_fifth_file,
    'metadata': initial_strand_metadata  # Reusing initial_strand_metadata for example
}

# Handle sixth_file_path
sixth_file_path = 'index.html'  # Replace with the actual path to your sixth file

def read_sixth_file(file_path):
    with open(file_path, 'r') as file:
        code_string = file.read()
    return code_string

# Read the content of the sixth file
plain_sixth_file = read_sixth_file(sixth_file_path)

# Add the content of the sixth file to the 'exons' entry in 'dna_structure'
dna_structure['html'] = {
    'code': plain_sixth_file,
    'metadata': initial_strand_metadata  # Reusing initial_strand_metadata for example
}

# Handle seventh_file_path
seventh_file_path = 'qros-dna-encoder.py'
def read_and_encode_seventh_file(file_path, rna_dna_mapper):
    with open(file_path, 'r') as file:
        code_string = file.read()
    encoded_code = rna_dna_mapper.map_body(code_string)
    return encoded_code

third_strand = {}

encoded_seventh_file = read_and_encode_seventh_file(seventh_file_path, rna_dna_mapper)
third_strand['encoded-encoder'] = encoded_seventh_file

# Handle eighth_file_path
eighth_file_path = 'qros-dna-decoder.py'
with open(eighth_file_path, 'r') as file:
    code_string = file.read()
encoded_eighth_file = rna_dna_mapper.map_body(code_string)

# Handle ninth_file_path
ninth_file_path = 'js-shell.html'  # Replace with the actual path to your ninth file

def read_ninth_file(file_path):
    with open(file_path, 'r') as file:
        code_string = file.read()
    return code_string

# Read the content of the ninth file
plain_ninth_file = read_ninth_file(ninth_file_path)

# Handle tenth_file_path
tenth_file_path = 'qros-dna-decoder.py'  # Replace with the actual path to your tenth file

def read_tenth_file(file_path):
    with open(file_path, 'r') as file:
        code_string = file.read()
    return code_string

# Read the content of the tenth file
plain_tenth_file = read_tenth_file(tenth_file_path)

third_strand = {
    'js-shell': plain_ninth_file,
    'encoded-encoder': encoded_seventh_file,
    'encoded-decoder': encoded_eighth_file,
    'decoder': plain_tenth_file,
    'metadata': initial_strand_metadata  # Reusing initial_strand_metadata for example
}

final_json_data['third_strand'] = third_strand

# Write to JSON
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(final_json_data, json_file, ensure_ascii=False, indent=4)

# Begin generating .png qr codes, 'chunks.json' and creating a qr code .mp4 video from 'encoded_dna_data.json'

import cv2
import numpy as np
import qrcode
import gzip
import base64
import os
import json
import time  # For adding delay

def generate_qr_code(data):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_cv = np.array(img.convert('RGB'))
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # Resize the image to 730x730
    img_cv = cv2.resize(img_cv, (730, 730))

    return img_cv

def compress_and_generate_base64_qr_images(file_path, chunk_size=1500):
    with open(file_path, 'rb') as f:
        data = f.read()

    compressed_data = gzip.compress(data)
    encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")

    print(f"Total size of base64 data before splitting: {len(encoded_data_base64)}")

    chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]

    # Write chunks to a JSON file
    with open('outputs/chunks.json', 'w') as json_file:
        json.dump({"chunks": chunks}, json_file)  # Save the chunks as an array within a JSON object

    os.makedirs('outputs/qrs', exist_ok=True)  # Create the directory if it doesn't exist

    for i, chunk in enumerate(chunks):
        print(f"Size of chunk {i}: {len(chunk)}")

        qr_img = generate_qr_code(chunk)

        cv2.imwrite(f'outputs/qrs/qr_{i:09d}.png', qr_img)  # Save each QR code as a PNG file

img_file_path = 'outputs/encoded_dna_data.json'
compress_and_generate_base64_qr_images(img_file_path)

# Add ffmpeg command to generate the video
os.system('ffmpeg -framerate 30 -i outputs/qrs/qr_%09d.png -vf "scale=730:730,setsar=1" -an -c:v libx264 -pix_fmt yuv420p outputs/encoded_dna_data.mp4')

# Begin decoding video file and generating 'decoded_encoded_dna_integrity.json'

import cv2
from pyzbar.pyzbar import decode
import base64
import gzip

# Open the video capture
video_capture = cv2.VideoCapture('outputs/encoded_dna_data.mp4')

def safe_base64_decode(data):
    if isinstance(data, str):
        # If data is already a string, it doesn't need to be decoded
        return data
    try:
        data = data.decode("utf-8")  # Decode the bytes to a string
    except UnicodeDecodeError:
        # If data is not valid UTF-8, it's probably already decoded
        return data
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception as e:
        print(f"Exception during decoding: {e}")
        print(f"Data: {data}")
        return None

# Initialize an empty list to hold the data from each QR code in the video
data_chunks = []
prev_chunk = None

while True:
    # Read a frame from the video
    ret, frame = video_capture.read()

    # Check if the frame was read successfully
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes from the frame
    decoded_objects = decode(gray_frame)

    # Process the decoded data and append to data_chunks
    for obj in decoded_objects:
        decoded_data = safe_base64_decode(obj.data)
        if decoded_data is not None and decoded_data != prev_chunk:
            data_chunks.append(decoded_data)
            prev_chunk = decoded_data

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Finished processing frames, releasing video capture...")
video_capture.release()

print("Concatenating and decompressing data...")
data = b''.join(data_chunks)

try:
    # Decompress the full data
    decompressed_data = gzip.decompress(data)
    with open("outputs/decoded/decoded_encoded_dna_integrity.json", "wb") as out_file:
        out_file.write(decompressed_data)
    print("Data decompressed and written to 'outputs/decoded/decoded_encoded_dna_integrity.json'.")
except Exception as e:
    print(f"Exception occurred during decompression: {e}")

print("Finished.")

qros-dna-decoder:

# Begin decoding and reconstruction of original files from encoded_dna_data.json

import os
import json
import ast  # For parsing string representation of a dictionary

os.makedirs('outputs/decoded', exist_ok=True)  # Create the directory if it doesn't exist

def reverse_mappings(mappings):
    return {value[1:]: key for key, value in mappings.items()}  # Remove the '_' prefix while reversing

def decode_body(body, reversed_mappings):
    # Sort the shorthand codes by length in descending order to avoid substring issues
    sorted_shorthands = sorted(reversed_mappings.keys(), key=len, reverse=True)
    for shorthand in sorted_shorthands:
        construct = reversed_mappings[shorthand]
        body = body.replace('_' + shorthand, construct)
    return body

# Step 1: Read the encoded_dna_data.json file
with open('outputs/encoded_dna_data.json', 'r') as json_file:
    encoded_dna_data = json.load(json_file)

# Extract encoded data and mappings
encoded_dna_structure = encoded_dna_data['dna_structure']['Genomes']['Chromosomes']['Genes']['Nucleotide Sequences']['code']
encoded_initial_strand = encoded_dna_data['initial_strand']['code']
encoded_second_strand = encoded_dna_data['second_strand']['code']
mappings_str = encoded_dna_data['dna_structure']['introns']['mappings']
non_encoded_fourth_file = encoded_dna_data['dna_structure']['exons']['code']  # New line for fourth file
non_encoded_fifth_file = encoded_dna_data['dna_structure']['files']['code']  # New line for fifth file
non_encoded_sixth_file = encoded_dna_data['dna_structure']['html']['code']  # New line for sixth file
encoded_third_strand = encoded_dna_data['third_strand']['encoded-encoder']
encoded_third_strand = encoded_dna_data['third_strand']['encoded-decoder']
non_encoded_ninth_file = encoded_dna_data['third_strand']['js-shell']

# Parse the string representation of mappings into a Python dictionary
mappings = ast.literal_eval(mappings_str)

# Step 2: Reverse the mappings
reversed_mappings = reverse_mappings(mappings)

# Step 3: Decode the data
decoded_dna_structure = decode_body(encoded_dna_structure, reversed_mappings)
decoded_initial_strand = decode_body(encoded_initial_strand, reversed_mappings)
decoded_second_strand = decode_body(encoded_second_strand, reversed_mappings)
decoded_third_strand = decode_body(encoded_second_strand, reversed_mappings)

# Step 4: Write the decoded content to new files
with open('outputs/decoded/decoded_qros-dna-readme.txt', 'w') as file:
    file.write(decoded_dna_structure)

with open('outputs/decoded/decoded_qros-dna-combos.sh', 'w') as file:
    file.write(decoded_initial_strand)

with open('outputs/decoded/decoded_qros-dna-txt-split.sh', 'w') as file:
    file.write(decoded_second_strand)

with open('outputs/decoded/decoded_web.js', 'w') as file:
    file.write(non_encoded_fourth_file)

with open('outputs/decoded/decoded_file-chunks.json', 'w') as file:
    file.write(non_encoded_fifth_file)

with open('outputs/decoded/decoded_html-index.html', 'w') as file:
    file.write(non_encoded_sixth_file)

with open('outputs/decoded/decoded_qros-dna-encoder.py', 'w') as file:
    file.write(decoded_third_strand)

with open('outputs/decoded/decoded_qros-dna-decoder.py', 'w') as file:
    file.write(decoded_third_strand)

with open('outputs/decoded/decoded_js-shell.html', 'w') as file:
    file.write(non_encoded_ninth_file)

# Begin chunks.json decoder
 
import json
import base64
import gzip

# Define the path to the 'chunks.json' file
chunks_json_path = 'outputs/chunks.json'

# Read the 'chunks.json' file to retrieve encoded data chunks
with open(chunks_json_path, 'r') as json_file:
    data = json.load(json_file)

# Extract the chunks from the JSON data
chunks = data.get('chunks', [])

# Initialize an empty list to hold decoded data chunks
decoded_chunks = []

# Decode each chunk from base64 and append to the list
for chunk in chunks:
    decoded_chunk = base64.urlsafe_b64decode(chunk)
    decoded_chunks.append(decoded_chunk)

# Concatenate the decoded chunks
concatenated_data = b''.join(decoded_chunks)

# Decompress the concatenated data using gzip
try:
    decompressed_data = gzip.decompress(concatenated_data)
except Exception as e:
    print(f"Exception occurred during decompression: {e}")
    decompressed_data = None

if decompressed_data is not None:
    # Define the path to the output file (the original file)
    output_file_path = 'outputs/decoded/decoded_chunks_file.json'

    # Write the decompressed data to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decompressed_data)

    print(f"Decompressed data written to '{output_file_path}'.")
else:
    print("Decompression failed. Check the input data.")

# Begin reconstruction of original files from decoded_chunks_file.json

import json
import ast  # For parsing string representation of a dictionary

def reverse_mappings(mappings):
    return {value[1:]: key for key, value in mappings.items()}  # Remove the '_' prefix while reversing

def decode_body(body, reversed_mappings):
    # Sort the shorthand codes by length in descending order to avoid substring issues
    sorted_shorthands = sorted(reversed_mappings.keys(), key=len, reverse=True)
    for shorthand in sorted_shorthands:
        construct = reversed_mappings[shorthand]
        body = body.replace('_' + shorthand, construct)
    return body

# Step 1: Read the encoded_dna_data.json file
with open('outputs/decoded/decoded_chunks_file.json', 'r') as json_file:
    encoded_dna_data = json.load(json_file)

# Extract encoded data and mappings
encoded_dna_structure = encoded_dna_data['dna_structure']['Genomes']['Chromosomes']['Genes']['Nucleotide Sequences']['code']
encoded_initial_strand = encoded_dna_data['initial_strand']['code']
encoded_second_strand = encoded_dna_data['second_strand']['code']
non_encoded_fourth_file = encoded_dna_data['dna_structure']['exons']['code']  # New line for fourth file
mappings_str = encoded_dna_data['dna_structure']['introns']['mappings']
non_encoded_fifth_file = encoded_dna_data['dna_structure']['files']['code']  # New line for fifth file
non_encoded_sixth_file = encoded_dna_data['dna_structure']['html']['code']  # New line for sixth file
encoded_third_strand = encoded_dna_data['third_strand']['encoded-encoder']
encoded_third_strand = encoded_dna_data['third_strand']['encoded-decoder']
non_encoded_ninth_file = encoded_dna_data['third_strand']['js-shell']

# Parse the string representation of mappings into a Python dictionary
mappings = ast.literal_eval(mappings_str)

# Step 2: Reverse the mappings
reversed_mappings = reverse_mappings(mappings)

# Step 3: Decode the data
decoded_dna_structure = decode_body(encoded_dna_structure, reversed_mappings)
decoded_initial_strand = decode_body(encoded_initial_strand, reversed_mappings)
decoded_second_strand = decode_body(encoded_second_strand, reversed_mappings)
decoded_third_strand = decode_body(encoded_third_strand, reversed_mappings)

# Step 4: Write the decoded content to new files
with open('outputs/decoded/decoded_qros-dna-chunks-readme.txt', 'w') as file:
    file.write(decoded_dna_structure)

with open('outputs/decoded/decoded_qros-dna-chunks-combos.sh', 'w') as file:
    file.write(decoded_initial_strand)

with open('outputs/decoded/decoded_qros-dna-chunks-txt-split.sh', 'w') as file:
    file.write(decoded_second_strand)

with open('outputs/decoded/decoded_chunks-web.js', 'w') as file:
    file.write(non_encoded_fourth_file)

with open('outputs/decoded/decoded_chunks-file-chunks.json', 'w') as file:
    file.write(non_encoded_fifth_file)

with open('outputs/decoded/decoded_chunks-index.html', 'w') as file:
    file.write(non_encoded_sixth_file)

with open('outputs/decoded/decoded_chunks-qros-dna-encoder.py', 'w') as file:
    file.write(decoded_third_strand)

with open('outputs/decoded/decoded_chunks-qros-dna-decoder.py', 'w') as file:
    file.write(decoded_third_strand)

with open('outputs/decoded/decoded_chunks-js-shell.html', 'w') as file:
    file.write(non_encoded_ninth_file)

# Begin final file extraction

import json
import base64
import gzip

# Define the path to the 'chunks.json' file
chunks_json_path = 'outputs/decoded/decoded_chunks-file-chunks.json'

# Read the 'chunks.json' file to retrieve encoded data chunks
with open(chunks_json_path, 'r') as json_file:
    data = json.load(json_file)

# Extract the chunks from the JSON data
chunks = data.get('chunks', [])

# Initialize an empty list to hold decoded data chunks
decoded_chunks = []

# Decode each chunk from base64 and append to the list
for chunk in chunks:
    decoded_chunk = base64.urlsafe_b64decode(chunk)
    decoded_chunks.append(decoded_chunk)

# Concatenate the decoded chunks
concatenated_data = b''.join(decoded_chunks)

# Decompress the concatenated data using gzip
try:
    decompressed_data = gzip.decompress(concatenated_data)
except Exception as e:
    print(f"Exception occurred during decompression: {e}")
    decompressed_data = None

if decompressed_data is not None:
    # Define the path to the output file (the original file)
    output_file_path = 'outputs/decoded/decoded_chunks_qros-dna.zip'

    # Write the decompressed data to the output file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decompressed_data)

    print(f"Decompressed data written to '{output_file_path}'.")
else:
    print("Decompression failed. Check the input data.")
