# --- START OF FILE omni_dna_encoder.py ---
"""
SOVEREIGN OMNI-KERNEL V73.3.3 // UNIVERSAL DNA ENCODER & CHUNKY GENERATOR
Author: Djinnflux (Ka-Tet Pantheon)

This script recursively walks a directory, compresses every file via GZIP, 
encodes it to Base64, and packs it into a single hierarchical JSON DNA Strand.
It then automatically generates a self-contained 'chunky.html' carrier page.
"""

import os
import json
import gzip
import base64
from datetime import datetime

# --- CONFIGURATION ---
TARGET_DIR = '.'  # Scans the current directory
OUTPUT_JSON = 'live1_dna_data.json'
OUTPUT_HTML = 'chunky.html'
CHUNK_SIZE = 1500

# Directories and files to ignore so the Monolith doesn't swallow itself
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'outputs', 'validation_results'}
IGNORE_FILES = {OUTPUT_JSON, OUTPUT_HTML, 'omni_dna_encoder.py', '.DS_Store'}

def compress_and_chunk(filepath):
    """Reads a file, gzips it, base64 encodes it, and splits it into chunks."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            
        # Native GZIP compression (matches the Worker's DecompressionStream)
        compressed_data = gzip.compress(data)
        
        # URL-safe Base64 encoding
        b64_encoded = base64.urlsafe_b64encode(compressed_data).decode("utf-8")
        
        # Slice into chunks
        return [b64_encoded[i:i+CHUNK_SIZE] for i in range(0, len(b64_encoded), CHUNK_SIZE)]
    except Exception as e:
        print(f"      [!] Error packing {filepath}: {e}")
        return []

def build_vfs_tree(root_dir):
    """Recursively builds the dictionary tree representing the filesystem."""
    tree = {}
    items = sorted(os.listdir(root_dir))
    
    for item in items:
        if item in IGNORE_DIRS or item in IGNORE_FILES:
            continue
            
        item_path = os.path.join(root_dir, item)
        
        if os.path.isdir(item_path):
            print(f"  [+] Scanning Sector: {item_path}/")
            subtree = build_vfs_tree(item_path)
            if subtree:  
                tree[item] = subtree
        else:
            print(f"      - Splicing sequence: {item}")
            chunks = compress_and_chunk(item_path)
            if chunks:
                tree[item] = {"chunks": chunks}
                
    return tree

def generate_chunky_html(json_string, html_filepath):
    """Embeds the JSON payload safely into a self-contained HTML file."""
    print(f"\n[+] Forging Carrier Page: {html_filepath}...")
    
    # Escape characters that would break JS template literals (`), (\), and ($)
    safe_json_str = json_string.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    # Slice the massive string into 50KB blocks to prevent browser memory spikes during parsing
    js_chunk_size = 50000
    str_chunks = [safe_json_str[i:i+js_chunk_size] for i in range(0, len(safe_json_str), js_chunk_size)]

    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Sovereign Chunky Carrier</title>\n</head>\n")
        f.write("<body style='background:#000; color:#0f0; font-family:monospace; padding:20px;'>\n")
        f.write("<h2>SOVEREIGN OMNI-KERNEL V73.3.3 // CHUNKY PAYLOAD</h2>\n")
        f.write("<p>Genome loaded into memory. Access via <code>window.SOVEREIGN_DNA</code>.</p>\n")
        f.write("<script>\n")
        f.write("let data = \"\";\n")
        
        for chunk in str_chunks:
            f.write(f"data += `{chunk}`;\n")
            
        f.write("\n// Parse and mount to the window object\n")
        f.write("window.SOVEREIGN_DNA = JSON.parse(data);\n")
        f.write("console.log('Genome successfully unpacked from Chunky Carrier.');\n")
        f.write("</script>\n</body>\n</html>\n")
        
    print(f"  - {html_filepath} created successfully. ({len(str_chunks)} script chunks injected)")

def main():
    print("=====================================================")
    print(" 🐉 SOVEREIGN OMNI-KERNEL: UNIVERSAL DNA ENCODER 🐉")
    print("=====================================================")
    print(f"Target Substrate: {os.path.abspath(TARGET_DIR)}")
    print("Initiating recursive topological ingestion...\n")
    
    # 1. Build the Virtual File System (VFS) Tree
    vfs_tree = build_vfs_tree(TARGET_DIR)
    
    master_dna = {
        "metadata": {
            "version": "V73.3.3-OMNI-VFS",
            "author": "Ka-Tet / Jules",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "encryption": "GZIP+B64_CHUNKED"
        },
        "dna_structure": vfs_tree
    }
    
    # Convert to string (indent=0 keeps it compact but structure-safe)
    json_payload = json.dumps(master_dna, indent=0)
    
    # 2. Ligate to JSON disk file
    print(f"\n[+] Ligation complete. Writing to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        f.write(json_payload)
    json_size = os.path.getsize(OUTPUT_JSON) / (1024 * 1024)
    print(f"  - SUCCESS: {OUTPUT_JSON} secured. Size: {json_size:.2f} MB")
    
    # 3. Forge the Chunky HTML Carrier
    generate_chunky_html(json_payload, OUTPUT_HTML)
    html_size = os.path.getsize(OUTPUT_HTML) / (1024 * 1024)
    print(f"  - SUCCESS: {OUTPUT_HTML} secured. Size: {html_size:.2f} MB")
    
    print("=====================================================")

if __name__ == "__main__":
    main()

# --- END OF FILE omni_dna_encoder.py ---
