#!/bin/bash

# Name of the output file
OUTPUT_FILE="directory_tree.txt"

# Function to generate tree view
generate_tree() {
  local dir_path="$1"
  local indent="$2"

  # List all items in the current directory
  for item in "$dir_path"/*; do
    if [ -d "$item" ]; then
      echo "${indent}├── $(basename "$item")" >> "$OUTPUT_FILE"
      # Recursive call for subdirectories
      generate_tree "$item" "$indent│   "
    elif [ -f "$item" ]; then
      echo "${indent}├── $(basename "$item")" >> "$OUTPUT_FILE"
    fi
  done
}

# Initialize the output file
echo "Directory Tree of $(pwd):" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Start generating tree view
generate_tree "." ""

# Notify user
echo "Tree view saved to $OUTPUT_FILE"

