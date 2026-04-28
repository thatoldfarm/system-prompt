import json
import os
import collections

# Define the directory and filenames
output_directory = 'outputs'
input_filename = 'encoded_dna_data.json'
new_filename = 'live_dna_data.json'

# Define the new Genome0 structure
new_genome_structure = {
    "kernel": {
        "version": "1.0",
        "tasks": [],
        "communicationBus": {},
        "metadata": {}
    },
    "dna_structure": {
        "Genomes": {
            "OS": {
                "v86": {},
                "kernel": {}
            },
            "FileSystem": {
                "SquashFS": {},
                "UserFiles": {}
            },
            "WebFrontEnd": {
                "HTML": {},
                "CSS": {},
                "JavaScript": {}
            },
            "WebBackEnd": {
                "ServerScripts": {},
                "Database": {}
            },
            "Desktop": {
                "UI": {},
                "Applications": {}
            }
        },
        "TemporaryStrands": []
    }
}

# Read the original encoded_dna_data.json
input_filepath = os.path.join(output_directory, input_filename)
with open(input_filepath, 'r') as f:
    original_data = json.load(f)

# Add the new Genome0 to the original data
dna_structure_dict = original_data['dna_structure']
if isinstance(dna_structure_dict, collections.OrderedDict):
    dna_structure_dict['Genome0'] = new_genome_structure
else:
    ordered_dna_structure = collections.OrderedDict(dna_structure_dict)
    ordered_dna_structure['Genome0'] = new_genome_structure
    original_data['dna_structure'] = ordered_dna_structure

# Write the modified data to live_dna_data.json
new_filepath = os.path.join(output_directory, new_filename)
with open(new_filepath, 'w') as f:
    json.dump(original_data, f, indent=4)
