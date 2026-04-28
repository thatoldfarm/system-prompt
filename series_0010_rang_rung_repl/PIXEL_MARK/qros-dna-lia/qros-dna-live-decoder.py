# --- START OF FILE qros-dna-live-decoder.py ---

"""
QROS-DNA Universal Validation Decoder (Final Version)

This script performs a comprehensive, multi-stage validation of all artifacts
produced by the QROS-DNA encoder. It can independently reconstruct the original
source files from all encoded formats, saving them with their original filenames.

PREREQUISITES:
You must install the required libraries before running this script:
pip install opencv-python pyzbar Pillow numpy
"""

import os
import json
import base64
import gzip
import ast
import re

# --- Dependency Check ---
try:
    import cv2
    from pyzbar.pyzbar import decode as qr_decode
    from PIL import Image
    import numpy as np
    OPTIONAL_LIBS_AVAILABLE = True
except ImportError:
    OPTIONAL_LIBS_AVAILABLE = False

# --- Configuration ---
MP4_INPUT_PATH = 'outputs/qros-dna-video.mp4'
GIF_INPUT_PATH = 'outputs/qros-dna-animated.gif'
QR_PNG_DIR = 'outputs/qrs'
CHUNKS_JSON_PATH = 'outputs/chunks.json'
MASTER_JSON_PATH = 'outputs/encoded_dna_data.json'
BINARY_CHUNKS_DIR = 'outputs/binary_chunks'
CHUNKY_HTML_PATH = 'outputs/chunky.html'
VALIDATION_ROOT_DIR = 'validation_results'


# --- CORE RECONSTRUCTION LOGIC ---

def reconstruct_files_from_master_json(master_json_data, output_dir):
    """
    The heart of the decoder. Takes a master JSON dictionary and an output directory,
    and reconstructs every single file with its original name.
    """
    print(f"  - Starting full reconstruction in '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)

    mappings = ast.literal_eval(master_json_data['dna_structure']['introns']['mappings'])
    reversed_mappings = {v[1:]: k for k, v in mappings.items()}

    def decode_text_body(encoded_body):
        sorted_symbols = sorted(reversed_mappings.keys(), key=len, reverse=True)
        for symbol in sorted_symbols:
            encoded_body = encoded_body.replace('_' + symbol, reversed_mappings[symbol])
        return encoded_body

    def write_file(path, content):
        with open(path, 'w', encoding='utf-8') as f: f.write(content)

    # --- DECODE AND SAVE WITH ORIGINAL FILENAMES ---
    # Encoded text files
    write_file(os.path.join(output_dir, 'qros-dna-readme.txt'), decode_text_body(master_json_data['dna_structure']['Genomes']['Chromosomes']['Genes']['Nucleotide Sequences']['code']))
    write_file(os.path.join(output_dir, 'qros-dna-combos.sh'), decode_text_body(master_json_data['initial_strand']['code']))
    write_file(os.path.join(output_dir, 'qros-dna-txt-split.sh'), decode_text_body(master_json_data['second_strand']['code']))
    write_file(os.path.join(output_dir, 'qros-dna-live-encoder.py'), decode_text_body(master_json_data['third_strand']['encoded-encoder']))
    write_file(os.path.join(output_dir, 'qros-dna-live-decoder.py'), decode_text_body(master_json_data['third_strand']['encoded-decoder']))
    
    # Non-encoded text files
    write_file(os.path.join(output_dir, '0web.js'), master_json_data['dna_structure']['exons']['0js'])
    write_file(os.path.join(output_dir, '0shell.html'), master_json_data['dna_structure']['exons']['0shell'])
    write_file(os.path.join(output_dir, '0index.html'), master_json_data['dna_structure']['exons']['0html'])
    write_file(os.path.join(output_dir, 'index.html'), master_json_data['dna_structure']['profusion']['code'])
    write_file(os.path.join(output_dir, 'js-shell.html'), master_json_data['third_strand']['js-shell'])
    write_file(os.path.join(output_dir, 'qros-dna-live-decoder.py'), master_json_data['third_strand']['decoder'])
    write_file(os.path.join(output_dir, 'async_load.html'), master_json_data['dna_structure']['emu']['loader'])
    write_file(os.path.join(output_dir, 'libv86.js'), master_json_data['dna_structure']['emu']['libv86'])
    
    # Reconstruct final binary files
    def reconstruct_binary(chunk_data_obj, output_path):
        chunk_data = json.loads(chunk_data_obj) if isinstance(chunk_data_obj, str) else chunk_data_obj
        chunks = chunk_data.get('chunks', [])
        concatenated_data = "".join(chunks).encode('utf-8')
        missing_padding = len(concatenated_data) % 4
        if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
        decompressed_data = gzip.decompress(base64.urlsafe_b64decode(concatenated_data))
        with open(output_path, 'wb') as f: f.write(decompressed_data)

    reconstruct_binary(master_json_data['dna_structure']['files']['code'], os.path.join(output_dir, 'qros-dna.zip'))
    reconstruct_binary(master_json_data['dna_structure']['emu']['v86wasm'], os.path.join(output_dir, 'v86.wasm'))
    print(f"  - SUCCESS: Full reconstruction complete in '{output_dir}'.")


# --- VALIDATION ROUTINES ---

def run_validation_from_visual_media(source_type, source_path, output_dir):
    print(f"\n--- VALIDATION {source_type.upper()}: DECODING FROM '{source_path}' ---")
    if not os.path.exists(source_path): print("  - [SKIPPED] Source file not found."); return
    seen_chunks, ordered_chunks = set(), []
    if source_type == 'mp4':
        cap = cv2.VideoCapture(source_path)
        while True:
            ret, frame = cap.read();
            if not ret: break
            data = qr_decode(frame)
            if data and data[0].data not in seen_chunks:
                seen_chunks.add(data[0].data); ordered_chunks.append(data[0].data)
        cap.release()
    elif source_type == 'gif':
        with Image.open(source_path) as img:
            for i in range(img.n_frames):
                img.seek(i); data = qr_decode(img)
                if data and data[0].data not in seen_chunks:
                    seen_chunks.add(data[0].data); ordered_chunks.append(data[0].data)
    if not ordered_chunks: print("  - [FAILURE] No QR codes could be decoded."); return
    concatenated_data = b"".join(ordered_chunks)
    missing_padding = len(concatenated_data) % 4
    if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
    master_json_data = json.loads(gzip.decompress(base64.urlsafe_b64decode(concatenated_data)).decode('utf-8'))
    reconstruct_files_from_master_json(master_json_data, output_dir)

def run_validation_from_qrs(source_dir, output_dir):
    print(f"\n--- VALIDATION PNGs: DECODING FROM '{source_dir}' ---")
    if not os.path.isdir(source_dir): print("  - [SKIPPED] Source directory not found."); return
    ordered_chunks = []
    files = sorted([f for f in os.listdir(source_dir) if f.endswith('.json')], key=lambda x: int(re.search(r'(\d+)\.json$', x).group(1)))
    for filename in files:
        with open(os.path.join(source_dir, filename), 'r') as f:
            chunk_data = json.load(f).get('chunk');
            if chunk_data: ordered_chunks.append(chunk_data.encode('utf-8'))
    if not ordered_chunks: print("  - [FAILURE] No data chunks found in JSON files."); return
    concatenated_data = b"".join(ordered_chunks)
    missing_padding = len(concatenated_data) % 4
    if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
    master_json_data = json.loads(gzip.decompress(base64.urlsafe_b64decode(concatenated_data)).decode('utf-8'))
    reconstruct_files_from_master_json(master_json_data, output_dir)
    
def run_validation_from_chunks_file(source_path, output_dir):
    print(f"\n--- VALIDATION CHUNKS.JSON: DECODING FROM '{source_path}' ---")
    if not os.path.exists(source_path): print("  - [SKIPPED] Source file not found."); return
    with open(source_path, 'r') as f: chunks = json.load(f).get('chunks', [])
    concatenated_data = "".join(chunks).encode('utf-8')
    missing_padding = len(concatenated_data) % 4
    if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
    master_json_data = json.loads(gzip.decompress(base64.urlsafe_b64decode(concatenated_data)).decode('utf-8'))
    reconstruct_files_from_master_json(master_json_data, output_dir)

def run_validation_from_master_json(source_path, output_dir):
    print(f"\n--- VALIDATION MASTER JSON: DECODING FROM '{source_path}' ---")
    if not os.path.exists(source_path): print("  - [SKIPPED] Source file not found."); return
    with open(source_path, 'r', encoding='utf-8') as f: master_json_data = json.load(f)
    reconstruct_files_from_master_json(master_json_data, output_dir)
    
def run_validation_from_binary_chunks(source_dir, output_dir):
    print(f"\n--- VALIDATION BINARY CHUNKS: DECODING FROM '{source_dir}' ---")
    if not os.path.isdir(source_dir): print("  - [SKIPPED] Source directory not found."); return
    os.makedirs(output_dir, exist_ok=True)
    files_to_reconstruct = {}
    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            base_name = filename.split('_chunks_chunk')[0]
            if base_name not in files_to_reconstruct: files_to_reconstruct[base_name] = []
            files_to_reconstruct[base_name].append(filename)
    for base_name, chunk_files in files_to_reconstruct.items():
        print(f"  - Reconstructing '{base_name}'...")
        sorted_files = sorted(chunk_files, key=lambda x: int(re.search(r'(\d+)\.json$', x).group(1)))
        chunks = [json.load(open(os.path.join(source_dir, f), 'r')).get('chunk', '') for f in sorted_files]
        concatenated_data = "".join(chunks).encode('utf-8')
        missing_padding = len(concatenated_data) % 4
        if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
        decompressed_data = gzip.decompress(base64.urlsafe_b64decode(concatenated_data))
        # --- CORRECTED: Use original filename for output ---
        output_path = os.path.join(output_dir, base_name)
        with open(output_path, 'wb') as f_out: f_out.write(decompressed_data)
        print(f"    - SUCCESS: Reconstructed '{os.path.basename(output_path)}'")

def run_validation_from_chunky_html(source_path, output_dir):
    print(f"\n--- VALIDATION CHUNKY.HTML: DECODING FROM '{source_path}' ---")
    if not os.path.exists(source_path): print("  - [SKIPPED] Source file not found."); return
    with open(source_path, 'r', encoding='utf-8') as f: html_content = f.read()
    pattern = re.compile(r"data \+= `(.*?)`;", re.DOTALL)
    json_strings = pattern.findall(html_content)
    if not json_strings: print("  - [FAILURE] No data chunks found in HTML file."); return
    
    grouped_chunks = {}
    for js_obj_str in json_strings:
        chunk_obj = json.loads(js_obj_str)
        file_identifier = chunk_obj.get("file")
        if file_identifier == "master_archive": # We only need the master archive to reconstruct everything
            chunk_content = chunk_obj.get("content", {}).get("chunk")
            if "master_archive" not in grouped_chunks: grouped_chunks["master_archive"] = []
            grouped_chunks["master_archive"].append(chunk_content)

    master_chunks = grouped_chunks.get("master_archive")
    if not master_chunks: print("  - [FAILURE] Could not find 'master_archive' chunks."); return
    
    concatenated_data = "".join(master_chunks).encode('utf-8')
    missing_padding = len(concatenated_data) % 4
    if missing_padding: concatenated_data += b'=' * (4 - missing_padding)
    master_json_data = json.loads(gzip.decompress(base64.urlsafe_b64decode(concatenated_data)).decode('utf-8'))
    reconstruct_files_from_master_json(master_json_data, output_dir)

# --- Main Execution ---
if __name__ == "__main__":
    print("--- QROS-DNA UNIVERSAL VALIDATION DECODER ---")
    if not OPTIONAL_LIBS_AVAILABLE:
        print("\n[FATAL ERROR] Required libraries not found. Please run: pip install opencv-python pyzbar Pillow numpy"); exit()

    os.makedirs(VALIDATION_ROOT_DIR, exist_ok=True)

    run_validation_from_visual_media('mp4', MP4_INPUT_PATH, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_mp4'))
    run_validation_from_visual_media('gif', GIF_INPUT_PATH, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_gif'))
    run_validation_from_qrs(QR_PNG_DIR, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_qrs'))
    run_validation_from_chunks_file(CHUNKS_JSON_PATH, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_chunks_json'))
    run_validation_from_master_json(MASTER_JSON_PATH, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_master_json'))
    run_validation_from_binary_chunks(BINARY_CHUNKS_DIR, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_binary_chunks'))
    run_validation_from_chunky_html(CHUNKY_HTML_PATH, os.path.join(VALIDATION_ROOT_DIR, 'reconstructed_from_chunky_html'))
    
    print("\n--- ALL VALIDATION ROUTINES COMPLETE ---")
    print(f"Check the '{VALIDATION_ROOT_DIR}' directory for all reconstructed outputs.")

# --- END OF FILE qros-dna-live-decoder.py ---
