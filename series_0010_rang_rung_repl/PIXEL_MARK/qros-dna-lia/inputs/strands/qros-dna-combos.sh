#!/bin/bash

characters=('T' 'A' 'C' 'G' 'Z')
output_file="dna-combinations.txt"
temp_file="temp_combinations.txt"
rm -f "$output_file" "$temp_file"

for i in "${characters[@]}"; do
    echo "_$i" >> "$temp_file"

    for j in "${characters[@]}"; do
        echo "_$i$j" >> "$temp_file"

        for k in "${characters[@]}"; do
            echo "_$i$j$k" >> "$temp_file"

            for l in "${characters[@]}"; do
                echo "_$i$j$k$l" >> "$temp_file"

                for m in "${characters[@]}"; do
                    echo "_$i$j$k$l$m" >> "$temp_file"
                done
            done
        done
    done
done

# Group combinations by length, alphabetize and sub-group
for length in {1..5}; do
    echo "Combinations of length $length:" >> "$output_file"
    grep -E "_[TAGCZ]{1,$length}$" "$temp_file" | sort >> "$output_file"
    echo >> "$output_file"  # Add a blank line after each group
done

# Clean up temp file
rm -f "$temp_file"

echo "Combinations generated and saved to $output_file."
