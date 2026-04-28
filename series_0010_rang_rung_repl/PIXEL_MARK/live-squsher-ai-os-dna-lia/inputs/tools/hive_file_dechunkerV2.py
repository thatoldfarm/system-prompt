import os
import json
import gzip
import base64
from collections import defaultdict

def get_chunk_number(filename):
    try:
        # The filename format is expected to be like 'AGRIC_chunks_chunk206.json'
        # We split by '_chunks_chunk' and then extract the number before '.json'
        parts = filename.split('_chunks_chunk')
        if len(parts) > 1:
            chunk_number_part = parts[1]
            return int(chunk_number_part.split('.')[0])
    except (IndexError, ValueError):
        # Log any issues with filename format
        print(f"Warning: Could not extract chunk number from filename '{filename}'")
    return -1

def format_output_filename(base_filename):
    # Format the output filename to have leading zeros
    return f"{base_filename}_decoded"

def decode_and_reconstruct(input_directory='outputs/chunks', output_directory='outputs/decoded'):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Group chunks by their original file names
    chunks_by_file = defaultdict(list)

    # Get a list of all JSON files in the input directory
    file_list = [f for f in os.listdir(input_directory) if f.endswith('.json')]

    for json_file_name in file_list:
        full_json_path = os.path.join(input_directory, json_file_name)

        # Read the JSON file
        with open(full_json_path, 'r') as json_file:
            data = json.load(json_file)

        # Extract the base filename and chunk number
        base_filename = json_file_name.split('_chunks_chunk')[0]
        chunk_number = get_chunk_number(json_file_name)

        if 'chunk' in data and chunk_number != -1:
            # Add the chunk to the list for its base file
            chunks_by_file[base_filename].append((chunk_number, data['chunk']))
        else:
            print(f"Skipping file {json_file_name} due to missing 'chunk' key or invalid chunk number.")

    # Process each group of chunks
    for base_filename, chunk_tuples in chunks_by_file.items():
        # Sort chunks by the chunk number
        sorted_chunk_data = [chunk_data for _, chunk_data in sorted(chunk_tuples)]

        # Concatenate the sorted chunks
        concatenated_base64_data = ''.join(sorted_chunk_data)

        # Decode the base64 data
        try:
            decoded_data = base64.urlsafe_b64decode(concatenated_base64_data)
        except Exception as e:
            print(f"Error decoding base64 data for {base_filename}: {e}")
            continue

        # Check if the decoded data starts with GZIP magic number
        if decoded_data[:2] != b'\x1f\x8b':
            print(f"File {base_filename} does not appear to be gzipped. Skipping.")
            continue

        # Decompress the data
        try:
            decompressed_data = gzip.decompress(decoded_data)
        except gzip.BadGzipFile as e:
            print(f"Error decompressing data for {base_filename}: {e}")
            continue

        # Format the output filename with leading zeros
        formatted_output_filename = format_output_filename(base_filename)

        # Write the reconstructed file
        output_file_path = os.path.join(output_directory, formatted_output_filename)
        with open(output_file_path, 'wb') as output_file:
            output_file.write(decompressed_data)

        print(f"Reconstructed file {formatted_output_filename} in {output_directory}")

if __name__ == "__main__":
    # Call the function to decode and reconstruct files
    decode_and_reconstruct()
