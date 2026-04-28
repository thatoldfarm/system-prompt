# QROS-DNA: A Persistent, Multi-Format Archival System

## Overview

The QROS-DNA project is a powerful and flexible toolchain for archiving a complete set of project files into a single, highly compressed, and structured data package. It goes beyond simple zipping by employing a unique, two-layer compression system and creating multiple output formats for maximum portability and data resilience, including visual media (GIF/MP4) and a self-contained HTML archive.

At its core, the system converts a directory of files into a master "blueprint" (a JSON file), compresses it, and then presents this archive in various formats. A universal validation decoder can then reverse the process from *any* of these formats to perfectly reconstruct the original files.

## Features

*   **Multi-Layer Compression:** Uses a custom, persistent "DNA" mapping to compress frequently used words in text files, in addition to standard `gzip` compression on the final archive.
*   **Persistent & Evolving Mapping:** The DNA map is saved between runs. The encoder learns from new source text and appends new mappings, becoming more efficient over time.
*   **Robust Streaming Architecture:** Handles very large files with a low memory footprint by processing them line-by-line.
*   **Multiple Output Formats:** Creates several artifacts from a single run:
    *   A monolithic `chunks.json` data archive.
    *   Individual QR code images for each data chunk.
    *   An animated GIF and an MP4 video of the QR code sequence.
    *   A self-contained `chunky.html` file for web-based distribution.
*   **Universal Validation Decoder:** A single, powerful script that can verify the integrity of the entire toolchain by reconstructing the original files from any of the generated artifacts.

---

## 1. Prerequisites & Setup

Before running the scripts, you must install the necessary external tools and Python libraries.

#### **A. Install External Tools**

This system requires `ffmpeg` for creating the MP4 video.

*   **On macOS (using Homebrew):** `brew install ffmpeg`
*   **On Debian/Ubuntu:** `sudo apt-get install ffmpeg`
*   **On Windows:** Download the binaries from [ffmpeg.org](https://ffmpeg.org) and add the `bin` directory to your system's PATH.

#### **B. Install Python Libraries**

Open your terminal and run this single command to install all required libraries for both the encoder and the full validation decoder:
```bash
pip install opencv-python pyzbar Pillow numpy qrcode[pil]
```

#### **C. File Structure**

The encoder expects a specific input directory structure. Create these folders and place your files inside them before running.

```
.
├── inputs/
│   ├── dna/
│   │   └── qros-dna-readme.txt  (This is the source for the DNA map)
│   ├── emu/
│   │   ├── async_load.html
│   │   ├── libv86.js
│   │   └── v86.wasm
│   ├── exons/
│   │   ├── 0index.html
│   │   ├── 0shell.html
│   │   └── 0web.js
│   ├── files/
│   │   └── qros-dna.zip
│   ├── profusion/
│   │   └── index.html
│   └── strands/
│       ├── js-shell.html
│       ├── qros-dna-combos.sh
│       └── qros-dna-txt-split.sh
├── qros-dna-live-encoder.py             (The Main Encoder)
└── qros-dna-live-decoder.py             (The Universal Decoder)
```

---

## 2. The Encoder: `qros-dna-live-encoder.py`

This is the main script that packages your project.

### How to Run

Simply execute the script from your terminal:
```bash
python3 qros-dna-live-encoder.py
```

### How It Works: The Multi-Stage Process

The encoder follows a sequence of carefully designed steps to build the archive.

#### **Stage 1: Pre-processing Binary Files**
The script first tackles binary files (`.zip`, `.wasm`) that cannot be text-encoded.
1.  **Compress:** Each binary file is compressed using `gzip`.
2.  **Encode:** The compressed binary data is encoded into a URL-safe `base64` string.
3.  **Chunk & Save:** This long string is split into smaller chunks, and each chunk is saved into its own JSON file inside `outputs/binary_chunks/`. The original filename is embedded in the chunk file's name (e.g., `qros-dna.zip_chunks_chunk001.json`), which is crucial for the `chunky.html` creation.

#### **Stage 2: Building the Persistent DNA Map**
This is the core of the custom text compression.
1.  **Load:** The script checks if `dna-mappings.txt` exists in the root directory. If so, it loads the existing word-to-symbol map.
2.  **Analyze:** It reads the `MAPPING_SOURCE_FILE` (`inputs/dna/qros-dna-readme.txt`) and counts the frequency of every word.
3.  **Append:** It identifies any frequently used words that are *not* already in the loaded map.
4.  **Generate & Resume:** It "fast-forwards" its DNA symbol generator past all known symbols and creates new, unique symbols (e.g., `_TA`, `_CGZ`) for the new words.
5.  **Save:** The complete map (old + new) is saved back to `dna-mappings.txt` and `dna-reverse-mappings.txt` in the root directory.

#### **Stage 3: Assembling the Master JSON Blueprint**
The script constructs the `encoded_dna_data.json` file.
1.  **Text Encoding:** It reads all text-based files (`.txt`, `.sh`, `.py`, etc.) and uses the final DNA map to replace common words with their short symbols.
2.  **Binary Embedding:** It reads the text content from the intermediate chunk files created in Stage 1.
3.  **Blueprint Creation:** It assembles all this data—the encoded text, the non-encoded text, the embedded binary data, and the full mapping dictionary—into a single, large, structured JSON file.

#### **Stages 4-7: Final Artifact Generation**
The script uses the master JSON file to create all the final outputs.
1.  **Monolithic Archive:** The master JSON is compressed and chunked into the main `outputs/chunks.json` archive.
2.  **Visual Media:** The chunks from the master archive are used to generate the individual QR code PNGs, the animated GIF, and the MP4 video.
3.  **Web Archive:** All chunk files (from both the binary files and the master archive) are embedded into the `outputs/chunky.html` file.

### Encoder Output Files Explained

The encoder creates the following files and directories:

*   **`dna-mappings.txt`**: (Root directory) A human-readable text file of the persistent forward map (`word` -> `_symbol`).
*   **`dna-reverse-mappings.txt`**: (Root directory) A human-readable text file of the reverse map (`_symbol` -> `word`).
*   **`outputs/`**: The main directory for all generated artifacts.
    *   **`binary_chunks/`**: Contains intermediate JSON files, one for each chunk of a processed binary file. The original filename is part of the chunk's name.
    *   **`qrs/`**: Contains individual QR code `.png` images and their corresponding `.json` chunk files, derived from the master archive.
    *   **`encoded_dna_data.json`**: The uncompressed master JSON "blueprint" file. This is the central piece of the archive.
    *   **`chunks.json`**: The final, monolithic, compressed data archive. This is a portable representation of the entire project.
    *   **`qros-dna-animated.gif`**: An animated GIF of the QR code sequence.
    *   **`qros-dna-video.mp4`**: An MP4 video of the QR code sequence, playable on any standard media player.
    *   **`chunky.html`**: A self-contained HTML file with all project data embedded in a JavaScript variable, ready for client-side decoding.

---

## 3. The Master JSON Blueprint Explained

The `encoded_dna_data.json` file is the "brain" of the archive. It uses biological metaphors to structure the data.

*   `"dna_structure"`: The main object containing the project's data.
    *   `"Genomes"` -> `"Chromosomes"` -> `"Genes"` -> `"Nucleotide Sequences"`: This nested structure holds the primary "DNA-encoded" content, typically from the main `readme.txt` file.
    *   `"introns"`: **Crucial.** This contains the complete `"mappings"` dictionary as a string. Like biological introns, this data is essential for processing (decoding) but isn't part of the final, readable output.
    *   `"exons"`: Contains files that were **not** DNA-encoded, such as JavaScript and HTML files. Like biological exons, this is "expressed" code that is included as-is.
    *   `"files"` & `"emu"`: These are additional containers for other non-encoded content, specifically the text representations of the original binary files (`qros-dna.zip`, `v86.wasm`).
*   `"initial_strand"`, `"second_strand"`, `"third_strand"`: These objects hold the content of other files that have been "DNA-encoded," such as shell scripts and the encoder/decoder source code itself.
*   `"metadata"`: Contains versioning information and a timestamp for the archive.

---

## 4. The Decoder: `qros-dna-live-decoder.py`

This is the universal validation script that proves the integrity of every artifact the encoder creates.

### How to Run

Simply execute the script from your terminal:```bash
python3 qros-dna-live-decoder.py
```

### What It Does: The Validation Process

The script performs a series of independent "round-trip" tests. For each test, it attempts to reconstruct the *entire original project* from a different starting artifact.

1.  **Test 1: Decode from MP4 Video:** Reads the `.mp4` file frame-by-frame, decodes the QR codes, and reconstructs all files.
2.  **Test 2: Decode from Animated GIF:** Does the same using the `.gif` file.
3.  **Test 3: Decode from Individual QR PNGs:** Scans the `outputs/qrs/` directory, combines the data from all chunk `.json` files, and reconstructs.
4.  **Test 4: Decode from `chunks.json`:** Uses the main monolithic archive to reconstruct.
5.  **Test 5: Decode from the Master JSON:** Uses the uncompressed `encoded_dna_data.json` file to reconstruct.
6.  **Test 6: Decode from Binary Chunks:** Specifically tests the intermediate binary chunk files from `outputs/binary_chunks/` by reconstructing just the original binary files.
7.  **Test 7: Decode from `chunky.html`:** Parses the `chunky.html` file, extracts the embedded JavaScript data, and reconstructs.

### Decoder Output Explained

The script creates a new root directory to store its results:

*   **`validation_results/`**: The main directory for all validation outputs.
    *   **`reconstructed_from_mp4/`**: The complete project, restored from the MP4 video.
    *   **`reconstructed_from_gif/`**: The project restored from the animated GIF.
    *   **`reconstructed_from_qrs/`**: The project restored from the individual QR code files.
    *   **`reconstructed_from_chunks_json/`**: The project restored from the main `chunks.json` archive.
    *   **`reconstructed_from_master_json/`**: The project restored from the uncompressed master JSON file.
    *   **`reconstructed_from_binary_chunks/`**: Contains only the binary files, restored from their intermediate chunks.
    *   **`reconstructed_from_chunky_html/`**: The project restored from the self-contained HTML archive.

If all these folders are successfully created and contain the original files, it provides a comprehensive validation of the entire system.
