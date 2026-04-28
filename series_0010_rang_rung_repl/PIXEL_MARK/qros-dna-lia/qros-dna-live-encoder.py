# --- START OF FILE qros-dna-live-encoder.py ---

import os
import json
import gzip
import base64
import re
import datetime
import itertools
import numpy as np
import shutil
import ast

# --- Dependency Check ---
try:
    import qrcode
    import cv2
    from PIL import Image
    OPTIONAL_LIBS_AVAILABLE = True
except ImportError:
    OPTIONAL_LIBS_AVAILABLE = False

print("--- QROS-DNA PERSISTENT ENCODER (OPTIMIZED + FULL EXPORTS + RESUMABLE MAP) ---")

# --- Configuration ---
MAPPING_SOURCE_FILE = 'inputs/dna/qros-dna-readme.txt'
# --- MODIFIED: Mapping files are now in the root directory for persistence ---
MAPPINGS_OUTPUT_FILE = 'dna-mappings.txt'
REVERSE_MAPPINGS_OUTPUT_FILE = 'dna-reverse-mappings.txt'

# Output directories remain the same
OUTPUT_DIR = 'outputs'
MASTER_JSON_PATH = os.path.join(OUTPUT_DIR, 'encoded_dna_data.json')
FINAL_CHUNKS_PATH = os.path.join(OUTPUT_DIR, 'chunks.json')
BINARY_CHUNKS_DIR = os.path.join(OUTPUT_DIR, 'binary_chunks')
QR_CODE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'qrs')
ANIMATED_GIF_PATH = os.path.join(OUTPUT_DIR, 'qros-dna-animated.gif')
MP4_VIDEO_PATH = os.path.join(OUTPUT_DIR, 'qros-dna-video.mp4')
CHUNKY_HTML_PATH = os.path.join(OUTPUT_DIR, 'chunky.html')
VIDEO_FRAME_RATE = 30

# --- Setup ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BINARY_CHUNKS_DIR, exist_ok=True)


# --- NEW FUNCTION: Load existing mappings from file ---
def load_existing_mappings(filepath):
    """Safely loads and parses the mappings file if it exists."""
    if not os.path.exists(filepath):
        print("  - No existing mapping file found. Will create a new one.")
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # ast.literal_eval is safer than eval for parsing Python data structures
            existing_map = ast.literal_eval(f.read())
            print(f"  - Found and loaded {len(existing_map)} existing mappings.")
            return existing_map
    except (SyntaxError, ValueError, FileNotFoundError):
        print(f"  - [WARNING] Could not parse existing map file '{filepath}'. Starting fresh.")
        return {}


# (Other core functions remain the same)
def compress_binary_file_for_json(file_path, output_dir, chunk_size=1500):
    base_filename = os.path.basename(file_path)
    print(f"  - Compressing binary file: {base_filename}")
    try:
        with open(file_path, 'rb') as f: data = f.read()
        compressed_data = gzip.compress(data)
        encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")
        chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]
        for index, chunk in enumerate(chunks):
            chunk_file_name = f"{base_filename}_chunks_chunk{index:03d}.json"
            json_file_path = os.path.join(output_dir, chunk_file_name)
            with open(json_file_path, 'w') as json_file: json.dump({"chunk": chunk}, json_file)
        print(f"    - Saved {len(chunks)} chunks to '{output_dir}'")
        return output_dir
    except FileNotFoundError:
        print(f"[ERROR] Binary file not found: {file_path}. Halting."); exit()

def finalize_and_generate_qr_chunks(input_file_path, chunk_size=1500):
    print(f"  - Compressing master JSON file: {os.path.basename(input_file_path)}")
    with open(input_file_path, 'rb') as f: data = f.read()
    compressed_data = gzip.compress(data)
    encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")
    chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]
    with open(FINAL_CHUNKS_PATH, 'w') as json_file: json.dump({"chunks": chunks}, json_file)
    print(f"  - Main archive created at: {FINAL_CHUNKS_PATH}")
    if not OPTIONAL_LIBS_AVAILABLE: print("\n[WARNING] Optional libraries not found. Skipping media generation."); return
    os.makedirs(QR_CODE_OUTPUT_DIR, exist_ok=True)
    print(f"  - Generating {len(chunks)} individual QR code PNG and JSON files...")
    for i, chunk in enumerate(chunks):
        chunk_file_name = f"master_archive_chunks_chunk{i:03d}.json"
        json_file_path = os.path.join(QR_CODE_OUTPUT_DIR, chunk_file_name)
        with open(json_file_path, 'w') as json_file: json.dump({"chunk": chunk}, json_file)
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(chunk); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_cv = np.array(img.convert('RGB')); img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
        img_cv = cv2.resize(img_cv, (730, 730))
        qr_image_path = os.path.join(QR_CODE_OUTPUT_DIR, f'qr_{i:09d}.png')
        cv2.imwrite(qr_image_path, img_cv)
    print(f"    - Successfully created all QR code and chunk files.")

def dna_symbol_generator():
    characters, length = ['T', 'A', 'C', 'G', 'Z'], 1
    while True:
        for combo in itertools.product(characters, repeat=length): yield "".join(combo)
        length += 1

def build_word_frequency_map(file_path):
    print(f"  - Building word frequency map from '{file_path}' (streaming)...")
    freq_map = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                words = re.findall(r'\b\w+\b', line)
                for word in words: freq_map[word.lower()] = freq_map.get(word.lower(), 0) + 1
    except FileNotFoundError:
        print(f"[ERROR] Mapping source file not found: {file_path}"); exit()
    return freq_map

class Optimized_RNA_DNA_Mapper:
    def __init__(self, mapping_dict):
        self.mapping = mapping_dict
        if not self.mapping: self.combined_pattern = None; return
        sorted_keys = sorted(self.mapping.keys(), key=len, reverse=True)
        pattern_str = r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b'
        self.combined_pattern = re.compile(pattern_str, re.IGNORECASE)
    def _get_replacement(self, match): return self.mapping[match.group(0).lower()]
    def map_body(self, body):
        return self.combined_pattern.sub(self._get_replacement, body) if self.combined_pattern else body

def stream_file_content(file_handle, input_path, mapper=None):
    file_handle.write('"')
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            for line in f_in:
                processed_line = mapper.map_body(line) if mapper else line
                file_handle.write(json.dumps(processed_line)[1:-1])
    except FileNotFoundError:
        print(f"\n[WARNING] File not found during streaming: {input_path}. Writing empty content.")
    file_handle.write('"')

def create_animated_gif_from_qrs(input_dir, output_path, frame_duration_ms=100):
    print(f"  - Assembling animated GIF from PNGs in '{input_dir}'...")
    images, target_size = [], (300, 300)
    blank_img = Image.new('RGB', target_size, (255, 255, 255)); images.append(blank_img)
    frame_count = 0
    png_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.png')])
    for filename in png_files:
        img = Image.open(os.path.join(input_dir, filename)).convert('RGB').resize(target_size)
        images.append(img); frame_count += 1
        if frame_count % 10 == 0: images.append(blank_img)
    images.append(blank_img)
    try:
        images[0].save(output_path, save_all=True, append_images=images[1:], duration=frame_duration_ms, loop=0)
        print(f"  - Animated GIF successfully created at: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to create animated GIF. Reason: {e}")

def create_mp4_from_qrs(input_dir, output_path, frame_rate):
    print(f"  - Assembling MP4 video from PNGs in '{input_dir}'...")
    if not shutil.which('ffmpeg'): print("\n[CRITICAL WARNING] `ffmpeg` command not found. Video creation skipped."); return
    input_pattern = os.path.join(input_dir, 'qr_%09d.png')
    command = (f'ffmpeg -y -framerate {frame_rate} -i "{input_pattern}" -vf "scale=730:730,setsar=1" -an -c:v libx264 -pix_fmt yuv420p "{output_path}"')
    os.system(command)
    print(f"  - MP4 video successfully created at: {output_path}")

def create_chunky_html(output_path, chunk_dirs):
    print(f"  - Assembling all chunks into '{output_path}'...")
    with open(output_path, 'w') as f_out:
        f_out.write('<!DOCTYPE html>\n<html><head><title>Chunky</title></head><body>\n<script>\nlet data = "";\n')
        for source_name, dir_path in chunk_dirs.items():
            if not os.path.isdir(dir_path): continue
            files = sorted([f for f in os.listdir(dir_path) if f.endswith('.json')], key=lambda x: int(re.search(r'(\d+)\.json$', x).group(1)))
            for file in files:
                file_identifier = file.split('_chunks_chunk')[0]
                with open(os.path.join(dir_path, file), 'r') as f_in: content = f_in.read()
                f_out.write(f"data += `{{\"source\": \"{source_name}\", \"file\": \"{file_identifier}\", \"content\": {content}}}`;\n")
        f_out.write('</script>\n</body></html>\n')
    print(f"  - Chunky.html has been created successfully.")


# --- Main Execution ---

# STAGE 1: Process Binary Files
print(">>> STAGE 1: Pre-processing binary files...")
compress_binary_file_for_json('inputs/files/qros-dna.zip', BINARY_CHUNKS_DIR)
compress_binary_file_for_json('inputs/emu/v86.wasm', BINARY_CHUNKS_DIR)
print(">>> STAGE 1 Complete.\n")

# --- STAGE 2: MODIFIED FOR PERSISTENT MAPPING ---
print(">>> STAGE 2: Building and updating the dynamic encoding maps...")
# 2.1: Load existing mappings if they exist
existing_mapping = load_existing_mappings(MAPPINGS_OUTPUT_FILE)

# 2.2: Build frequency map from the source file
word_freq = build_word_frequency_map(MAPPING_SOURCE_FILE)
words_to_encode = {word for word, count in word_freq.items() if count >= 2}

# 2.3: Determine which words are new and need a symbol
new_words = sorted(list(words_to_encode - set(existing_mapping.keys())), key=lambda word: (-word_freq[word], word))

# 2.4: Fast-forward the symbol generator past all existing symbols
symbol_gen = dna_symbol_generator()
if existing_mapping:
    print("  - Fast-forwarding symbol generator to resume from last session...")
    # Sort symbols by length, then alphabetically to find the true "last" one
    existing_symbols = [s.strip('_') for s in existing_mapping.values()]
    last_symbol = sorted(existing_symbols, key=lambda s: (len(s), s))[-1]
    for symbol in symbol_gen:
        if symbol == last_symbol:
            break

# 2.5: Generate mappings for new words only
if new_words:
    print(f"  - Found {len(new_words)} new words to add to the map.")
    new_mappings = {word: f"_{next(symbol_gen)}" for word in new_words}
    existing_mapping.update(new_mappings) # Append new mappings to the old ones
else:
    print("  - No new words found. The existing map is up-to-date.")

final_mapping = existing_mapping

# 2.6: Save the final, updated mapping files to the root directory
print(f"  - Saving {len(final_mapping)} total forward mappings to '{MAPPINGS_OUTPUT_FILE}'...")
with open(MAPPINGS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("{\n")
    mapping_items = list(final_mapping.items())
    for i, (word, code) in enumerate(mapping_items): f.write(f"  '{word}':'{code}'" + ("," if i < len(mapping_items) - 1 else "") + "\n")
    f.write("}\n")

reverse_mapping = {v: k for k, v in final_mapping.items()}
print(f"  - Saving {len(reverse_mapping)} reverse mappings to '{REVERSE_MAPPINGS_OUTPUT_FILE}'...")
with open(REVERSE_MAPPINGS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("{\n")
    mapping_items = list(reverse_mapping.items())
    for i, (code, word) in enumerate(mapping_items): f.write(f"  '{code}':'{word}'" + ("," if i < len(mapping_items) - 1 else "") + "\n")
    f.write("}\n")

rna_dna_mapper = Optimized_RNA_DNA_Mapper(final_mapping)
print(f"  - Optimized map and regex engine created.")
print(">>> STAGE 2 Complete.\n")

# STAGE 3: Build Master JSON using Streaming
print(f">>> STAGE 3: Streaming all data into '{MASTER_JSON_PATH}'...")
def get_chunk_text_from_dir(dir_path, filename_prefix):
    chunks_content = []
    files = sorted([f for f in os.listdir(dir_path) if f.startswith(filename_prefix)], key=lambda x: int(re.search(r'(\d+)\.json$', x).group(1)))
    for file in files:
        with open(os.path.join(dir_path, file), 'r') as f: chunks_content.append(json.load(f).get('chunk', ''))
    return json.dumps({"chunks": chunks_content})
zip_chunks_text = get_chunk_text_from_dir(BINARY_CHUNKS_DIR, 'qros-dna.zip')
wasm_chunks_text = get_chunk_text_from_dir(BINARY_CHUNKS_DIR, 'v86.wasm')

current_timestamp = datetime.datetime.now().isoformat()
metadata_str = json.dumps({'version': '9.0-persistent-map', 'author': 'AI', 'timestamp': current_timestamp}, indent=4)
with open(MASTER_JSON_PATH, 'w', encoding='utf-8') as f:
    f.write('{\n"dna_structure": {\n')
    f.write('  "Genomes": { "Chromosomes": { "Genes": { "Nucleotide Sequences": { "code": '); stream_file_content(f, 'inputs/dna/qros-dna-readme.txt', rna_dna_mapper)
    f.write('}}}},\n  "introns": { "mappings": ' + json.dumps(str(final_mapping)) + ' },\n  "exons": {\n    "0js": '); stream_file_content(f, 'inputs/exons/0web.js')
    f.write(',\n    "0shell": '); stream_file_content(f, 'inputs/exons/0shell.html')
    f.write(',\n    "0html": '); stream_file_content(f, 'inputs/exons/0index.html')
    f.write('\n  },\n  "files": { "code": ' + zip_chunks_text + ' },\n')
    f.write('  "profusion": { "code": '); stream_file_content(f, 'inputs/profusion/index.html')
    f.write(' },\n  "emu": {\n    "loader": '); stream_file_content(f, 'inputs/emu/async_load.html')
    f.write(',\n    "libv86": '); stream_file_content(f, 'inputs/emu/libv86.js')
    f.write(',\n    "v86wasm": ' + wasm_chunks_text + '\n  }\n},\n')
    f.write('"initial_strand": {\n  "code": '); stream_file_content(f, 'inputs/strands/qros-dna-combos.sh', rna_dna_mapper)
    f.write(f',\n  "metadata": {metadata_str}\n')
    f.write('},\n"second_strand": {\n  "code": '); stream_file_content(f, 'inputs/strands/qros-dna-txt-split.sh', rna_dna_mapper)
    f.write(f',\n  "metadata": {metadata_str}\n')
    f.write('},\n"third_strand": {\n  "js-shell": '); stream_file_content(f, 'inputs/strands/js-shell.html')
    f.write(',\n  "encoded-encoder": '); stream_file_content(f, __file__, rna_dna_mapper)
    f.write(',\n  "encoded-decoder": '); stream_file_content(f, 'qros-dna-live-decoder.py', rna_dna_mapper)
    f.write(',\n  "decoder": '); stream_file_content(f, 'qros-dna-live-decoder.py')
    f.write(f',\n  "metadata": {metadata_str}\n')
    f.write('}\n}\n')
print("  - Master JSON file has been written successfully.")
print(">>> STAGE 3 Complete.\n")

# STAGE 4: Final Compression and Chunk Generation
print(f">>> STAGE 4: Finalizing archive and generating all chunk types...")
finalize_and_generate_qr_chunks(MASTER_JSON_PATH)
print(">>> STAGE 4 Complete.\n")

# STAGE 5: Create Animated GIF
print(">>> STAGE 5: Creating Animated GIF from QR chunks...")
if OPTIONAL_LIBS_AVAILABLE and os.path.isdir(QR_CODE_OUTPUT_DIR) and any(f.endswith('.png') for f in os.listdir(QR_CODE_OUTPUT_DIR)):
    create_animated_gif_from_qrs(QR_CODE_OUTPUT_DIR, ANIMATED_GIF_PATH, frame_duration_ms=100)
else: print("  - Skipping GIF creation.")
print(">>> STAGE 5 Complete.\n")

# STAGE 6: Create MP4 Video
print(">>> STAGE 6: Creating MP4 Video from QR chunks...")
if OPTIONAL_LIBS_AVAILABLE and os.path.isdir(QR_CODE_OUTPUT_DIR) and any(f.endswith('.png') for f in os.listdir(QR_CODE_OUTPUT_DIR)):
    create_mp4_from_qrs(QR_CODE_OUTPUT_DIR, MP4_VIDEO_PATH, VIDEO_FRAME_RATE)
else: print("  - Skipping MP4 creation.")
print(">>> STAGE 6 Complete.\n")

# STAGE 7: Create Chunky HTML File
print(">>> STAGE 7: Creating self-contained Chunky HTML file...")
if OPTIONAL_LIBS_AVAILABLE:
    chunk_directories_to_include = { "binary_chunks": BINARY_CHUNKS_DIR, "master_archive": QR_CODE_OUTPUT_DIR }
    create_chunky_html(CHUNKY_HTML_PATH, chunk_directories_to_include)
else: print("  - Skipping Chunky HTML creation.")
print(">>> STAGE 7 Complete.\n")

print("--- ALL PROCESSES COMPLETE ---")
