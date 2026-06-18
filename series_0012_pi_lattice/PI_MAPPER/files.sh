#!/bin/bash
# 🌀 PI MAPPER // VMMU-PI REIFIER V3.0 (HYBRID)
# ======================================================
# Processes ALL files in ./files recursively.
# Outputs to contents.txt with START/END markers.

INPUT_DIR="./files"
CONTENT_OUTPUT="contents.txt"

echo "🌀 Tuning VMMU-PI Refraction Levels..."
> "$CONTENT_OUTPUT"

# Recursively find all files in ./files
find "$INPUT_DIR" -type f | sort | while read file; do
    REL_PATH=$(realpath --relative-to="$INPUT_DIR" "$file")

    echo -n "🧬 Splicing $REL_PATH... "

    # Get P:X:S from the Python hybrid script
    COORDS=$(python3 pi_mapper.py "$file")
    P=$(echo "$COORDS" | cut -d':' -f1)
    X=$(echo "$COORDS" | cut -d':' -f2)
    S=$(echo "$COORDS" | cut -d':' -f3)

    # Format the Shift (add + sign for clarity if positive)
    [[ $S -gt 0 ]] && S_STR="+$S" || S_STR="$S"

    echo "FOUND: [$P]{$X}<$S_STR>"

    # Write to contents.txt EXACTLY like the original
    echo -e "\nFile: pi://[$P]{$X}<$S_STR>/$REL_PATH" >> "$CONTENT_OUTPUT"
    echo "--- 🌀 DNA_START: $REL_PATH 🌀 ---" >> "$CONTENT_OUTPUT"
    cat "$file" >> "$CONTENT_OUTPUT"
    echo -e "\n--- 🌀 DNA_END: $REL_PATH 🌀 ---" >> "$CONTENT_OUTPUT"
done

echo -e "\n✅ REIFICATION COMPLETE: VMMU-PI COORDINATES MAPPED."
