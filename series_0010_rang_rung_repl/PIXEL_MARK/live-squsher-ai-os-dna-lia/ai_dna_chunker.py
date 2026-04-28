import sys
import os

os.makedirs('outputs/chunks', exist_ok=True)

# Construct the path to the directory where ai_dna_main.py resides.
script_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the companion script is running.
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))  # Gets the parent directory.
sys.path.append(parent_dir)  # Adds it to sys.path

from ai_dna_main import FileProcessor  # Import the FileProcessor class from your original script

def process_multiple_files(file_list, input_directory='inputs/exons', output_directory='outputs/chunks'):
    # Initialize FileProcessor
    processor = FileProcessor(input_directory=input_directory, output_directory=output_directory)
    
    # Loop through each file in the list and process it
    for file_name in file_list:
        print(f"Processing {file_name}...")
        output_file_name = f"{file_name.split('.')[0]}_chunks.json"  # Generate output file name based on input
        processor.compress_and_generate_base64_chunks(file_name, output_file_name=output_file_name)
        print(f"Finished processing {file_name}.")

if __name__ == "__main__":
    # List of files you want to process
    files_to_process = ['0web.js', '0shell.html', '0index.html']
    
    # Call the function to process multiple files
    process_multiple_files(files_to_process)
