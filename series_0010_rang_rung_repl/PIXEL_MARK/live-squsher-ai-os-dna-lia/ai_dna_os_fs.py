import json

def add_genome0_to_dna_structure(encoded_dna_file_path, chunks_file_path, output_file_path):
    # Read the original encoded_dna_data.json file
    with open(encoded_dna_file_path, 'r') as f:
        encoded_dna_data = json.load(f)
    
    # Read the chunks file (outputs_chunks.json)
    with open(chunks_file_path, 'r') as f:
        chunks_data = json.load(f)
    
    # Create the Genome0 structure
    genome0 = {
        "Genome0": {
            "Kernel": {
                "version": "1.0",
                "tasks": [],
                "communicationBus": {},
                "metadata": {}
            },
            "OS": {
                "v86": {},
                "Kernel": {}
            },
            "FileSystem": {},  # Inserting the chunk content here

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
        }
    
    # Add Genome0 to the dna_structure
    if 'dna_structure' in encoded_dna_data:
        encoded_dna_data['dna_structure'].update(genome0)
    
    # Replace the FileSystem placeholder with the actual chunks data
    encoded_dna_data['dna_structure']['Genome0']['FileSystem'] = chunks_data
    
    # Serialize most of the JSON structure
    with open(output_file_path, 'w') as f:
        json.dump(encoded_dna_data, f, indent=4)
    
    # Now let's rewrite the file to put FileSystem content on a single line
    with open(output_file_path, 'r') as f:
        lines = f.readlines()
    
    with open(output_file_path, 'w') as f:
        in_filesystem = False
        for line in lines:
            if '"FileSystem": {' in line:
                in_filesystem = True
                f.write(line.rstrip() + json.dumps(chunks_data)[1:] + '\n')
                continue
            if in_filesystem and '}' in line:
                in_filesystem = False
                continue
            if not in_filesystem:
                f.write(line)

# Paths to the relevant files
encoded_dna_file_path = 'outputs/live_dna_data.json'  # Replace with the path to your encoded_dna_data.json
chunks_file_path = 'outputs/chunks/outputs_chunks.json'  # Replace with the path to your chunks.json
output_file_path = 'outputs/live0_dna_data.json'  # Replace with the path where you want to save the new json file

# Call the function
add_genome0_to_dna_structure(encoded_dna_file_path, chunks_file_path, output_file_path)