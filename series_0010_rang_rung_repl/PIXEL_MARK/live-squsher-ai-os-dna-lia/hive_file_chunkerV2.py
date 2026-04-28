import sys
import os
import json
import datetime
import os
import gzip
import base64


# Ensure the output directory exists
os.makedirs('outputs/chunks', exist_ok=True)
os.makedirs('outputs/decoded', exist_ok=True)

# Construct the path to the directory where qros_dna_main.py resides.
script_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the companion script is running.
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))  # Gets the parent directory.
sys.path.append(parent_dir)  # Adds it to sys.path

class FileProcessor:
    def __init__(self, input_directory='inputs', output_directory='outputs'):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def compress_and_generate_base64_chunks(self, file_name):
        file_path = os.path.join(self.input_directory, file_name)
        
        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            data = f.read()

        # Compress the data using GZIP
        compressed_data = gzip.compress(data)

        # Encode the compressed data to base64
        encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")

        # Split the base64 data into chunks of approximately 65536 characters
        # The 65536 value is the characters that can be written to a single block on the Hive blockchain
        # For testing purposes the value is set lower as error mitigation  
        chunk_size = 64536  # Adjusted size to account for base64 encoding
        chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]

        # Write each chunk to a separate file
        for index, chunk in enumerate(chunks):
            # Format the chunk index to have leading zeros
            chunk_index_str = f"{index:03d}"
            chunk_file_name = f"{file_name}_chunks_chunk{chunk_index_str}.json"  # Keep full file name including extension
            json_file_path = os.path.join(self.output_directory, chunk_file_name)
            with open(json_file_path, 'w') as json_file:
                json.dump({"chunk": chunk}, json_file)
            print(f"Chunk {chunk_index_str} has been saved to {json_file_path}")

def process_multiple_files(input_directory='inputs', output_directory='outputs/chunks'):
    # Initialize FileProcessor
    processor = FileProcessor(input_directory=input_directory, output_directory=output_directory)

    # Get a list of all files in the input directory
    file_list = os.listdir(input_directory)

    # Loop through each file in the list and process it
    for file_name in file_list:
        # Check if the file is not a directory
        if not os.path.isdir(os.path.join(input_directory, file_name)):
            print(f"Processing {file_name}...")
            processor.compress_and_generate_base64_chunks(file_name)
            print(f"Finished processing {file_name}.")

if __name__ == "__main__":
    # Call the function to process all files in the specified directory
    process_multiple_files()
