# Import Section: Import all the required modules here
import re
import json
import datetime
import os
import gzip
import base64
import subprocess

os.makedirs('outputs/chunks', exist_ok=True)

# Class Definitions

## FileProcessing: This class is used to read and process text files.
### Example Usage: 
### processed_text = FileProcessing.read_and_process_file('path/to/your/file.txt')
class FileProcessing:
    @staticmethod
    def read_and_process_file(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        lines = [line.strip().lower() for line in lines if line.strip()]
        return ' '.join(lines)

class MappingGenerator:
    def __init__(self, input_file_path, output_dir):
        self.input_file_path = input_file_path
        self.output_dir = output_dir
        self.characters = ['T', 'A', 'C', 'G', 'Z']
        self.generated_mappings = []
        self.word_frequency_filtered = {}
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_mappings(self):
        combinations = [f"{char}" for char in self.characters]
        self.generated_mappings.extend(combinations)

        # Generate mappings for combinations of two characters
        combinations = [f"{char1}{char2}" for char1 in self.characters for char2 in self.characters]
        self.generated_mappings.extend(combinations)

        # Generate mappings for combinations of three characters
        combinations = [f"{char1}{char2}{char3}" for char1 in self.characters for char2 in self.characters for char3 in self.characters]
        self.generated_mappings.extend(combinations)

        # Generate mappings for combinations of four characters
        combinations = [f"{char1}{char2}{char3}{char4}" for char1 in self.characters for char2 in self.characters for char3 in self.characters for char4 in self.characters]
        self.generated_mappings.extend(combinations)

        # Generate mappings for combinations of five characters
        combinations = [f"{char1}{char2}{char3}{char4}{char5}" for char1 in self.characters for char2 in self.characters for char3 in self.characters for char4 in self.characters for char5 in self.characters]
        self.generated_mappings.extend(combinations)

    def read_and_count_words(self):
        with open(self.input_file_path, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    word = re.sub(r'[^\w\s]', '', word).lower()
                    if word.strip():
                        self.word_frequency_filtered[word] = self.word_frequency_filtered.get(word, 0) + 1

    def filter_and_write_mappings(self):
        words_filtered = {word: count for word, count in self.word_frequency_filtered.items() if count >= 2}
        with open(f"{self.output_dir}/dna-mappings.txt", 'w') as file:
            file.write("{\n")
            for word, code in zip(words_filtered, self.generated_mappings):
                file.write(f"  '{word}':'_{code}',\n")
            file.write("}\n")

    def generate_reverse_mappings(self):
        with open(f"{self.output_dir}/dna-mappings.txt", 'r') as file:
            mapping = eval(file.read())
        reverse_mapping = {v.strip("'_"): k for k, v in mapping.items()}
        with open(f"{self.output_dir}/dna-reverse-mappings.txt", 'w') as file:
            file.write("{\n")
            for code, word in reverse_mapping.items():
                file.write(f"  '_{code}':'{word}',\n")
            file.write("}\n")

## RNA_DNA_Mapper: This class maps words to DNA sequences.
### Example Usage:
### mapper = RNA_DNA_Mapper(generated_mappings, word_frequency_filtered)
### mapped_string = mapper.map_body('your text here')

class RNA_DNA_Mapper:
    def __init__(self, generated_mappings, word_frequency_filtered):
        self.mapping = {word: f"_{code}" for word, code in zip(word_frequency_filtered.keys(), generated_mappings)}
    
    def map_body(self, body):
        original_body = body
        for construct, shorthand in self.mapping.items():
            replaced_body = re.sub(r'\b' + re.escape(construct) + r'\b', shorthand, body)
            if replaced_body != body:
                print(f"Replaced: {construct} -> {shorthand}")
            body = replaced_body
        if original_body == body:
            print("All mappings used. Appending remaining content as-is.")
        return body

class FileProcessor:
    def __init__(self, input_directory='inputs', output_directory='outputs'):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def compress_and_generate_base64_chunks(self, file_name, chunk_size=1500, output_file_name=None):
        file_path = os.path.join(self.input_directory, file_name)
        
        # Create directory if it doesn't exist
        json_file_dir = os.path.join(self.output_directory, os.path.dirname(file_name))
        os.makedirs(json_file_dir, exist_ok=True)
        
        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            data = f.read()

        # Compress the data using GZIP
        compressed_data = gzip.compress(data)

        # Encode the compressed data to base64
        encoded_data_base64 = base64.urlsafe_b64encode(compressed_data).decode("utf-8")

        print(f"Total size of base64 data before splitting: {len(encoded_data_base64)}")

        # Split the base64 data into chunks
        chunks = [encoded_data_base64[i:i+chunk_size] for i in range(0, len(encoded_data_base64), chunk_size)]

        # Determine the output file name
        final_output_file_name = output_file_name if output_file_name else f'{file_name}-ai-dna.json'
        
        # Write chunks to a JSON file
        json_file_path = os.path.join(self.output_directory, final_output_file_name)
        with open(json_file_path, 'w') as json_file:
            json.dump({"chunks": chunks}, json_file)  # Save the chunks as an array within a JSON object

        print(f"Chunks have been saved to {json_file_path}")
  
## CodeParser: This class reads, cleans, and processes files for further actions.
### Example Usage:
### parser = CodeParser('input/file/path', 'output/file/path', RNA_DNA_Mapper_instance)
### parser.create_code_entry()

class CodeParser:
    def __init__(self, file_path, output_path, rna_dna_mapper):
        self.file_path = file_path
        self.output_path = output_path
        self.rna_dna_mapper = rna_dna_mapper
    
    def read_and_clean_file(self):
        cleaned_code_lines = []
        in_block_comment = False
        with open(self.file_path, 'r') as file:
            for line in file:
                if '"""' in line or "'''" in line:
                    in_block_comment = not in_block_comment
                    cleaned_code_lines.append(line)
                    continue
                if in_block_comment:
                    cleaned_code_lines.append(line)
                    continue
                cleaned_line = re.sub(r'#.*$', '', line)
                cleaned_code_lines.append(cleaned_line)
        return ''.join(cleaned_code_lines)

    def create_code_entry(self):
        code_string = self.read_and_clean_file()
        if self.rna_dna_mapper:
            code_string = self.rna_dna_mapper.map_body(code_string)
            code_entry = {'code': code_string}
        return code_entry

    def write_code_entry_to_json(self, code_entry):
        with open(self.output_path, 'w', encoding='utf-8') as json_file:
            json.dump(code_entry, json_file, ensure_ascii=False, indent=4)

# Initial Configuration: Set initial variables and instances here.
generated_mappings = []
word_frequency_filtered = {}
file_path = 'inputs/dna/ai-dna-readme.txt'
output_path = 'outputs/encoded_dna_data.json'

# Main Function: Wraps all of the above code to ensure it's only run when this script is executed directly.
# Other class definitions and import statements remain the same

def main():
    # Initialize the MappingGenerator
    mg = MappingGenerator('inputs/dna/ai-dna-readme.txt', 'outputs')
    mg.generate_mappings()
    mg.read_and_count_words()
    mg.filter_and_write_mappings()
    mg.generate_reverse_mappings()

    # Initialize the RNA_DNA_Mapper
    rna_dna_mapper = RNA_DNA_Mapper(mg.generated_mappings, mg.word_frequency_filtered)

    # Define the path to the 'ai_dna_main.py' file
    ai_dna_main_path = os.path.join(os.path.dirname(__file__), 'ai_dna_main.py')

    # Read the content of 'ai-dna-main.py' file
    with open(ai_dna_main_path, 'r', encoding='utf-8') as main_script_file:
        main_script_content = main_script_file.read()

    # Initialize the CodeParser
    parser = CodeParser('inputs/dna/ai-dna-readme.txt', 'outputs/encoded_dna_data.json', rna_dna_mapper)

    # Here is where you should call the method on parser
    initial_strand_code_entry = parser.create_code_entry()
    initial_strand_code = main_script_content  # Replace with the content of 'ai-dna-main.py'
    initial_strand_code = rna_dna_mapper.map_body(initial_strand_code)

    dna_structure_code_entry = parser.create_code_entry()
    dna_structure_code = dna_structure_code_entry['code']
    dna_structure_code = rna_dna_mapper.map_body(dna_structure_code)

    os.makedirs('outputs', exist_ok=True)  # Create the directory if it doesn't exist
    os.makedirs('outputs/decoded', exist_ok=True)  # Create the directory if it doesn't exist

    # Initialize the FileProcessor
    processor = FileProcessor()

    # List of files to process
    files_to_process = ['exons/0index.html', 'exons/0web.js', 'exons/0shell.html']

    exons_data = {}
    # Loop over each file and process it
    for file_name in files_to_process:
        processed_data = FileProcessing.read_and_process_file(os.path.join(processor.input_directory, file_name))
        exon_key = os.path.basename(file_name).split('.')[0]  # Extracting the file name without extension
        exons_data[exon_key] = processed_data

    current_timestamp = datetime.datetime.now().isoformat()
    # Your existing initial_strand_metadata dictionary
    initial_strand_metadata = {
        'metadata': {
            'persistenceFlag': 'true',
            'version': '1.0',
            'author': 'AI',
            'description': 'DNA strand with metadata and versioning',
            'timestamp': "current_timestamp"  # Replace with actual timestamp
        },
        'kernel0': {
            'trigger': {
                'script': "console.log('Trigger activated');"
            }
        }
    }

    # The new kernel dictionary you want to add
    new_kernel1_data = {
        "kernel1": {
            "trigger": {
                "action": "print",
                "data": "This is a trigger",
                "annotation": "execute_on_read"
            }
        }
    }

    # Add new_kernel1_data to initial_strand_metadata
    initial_strand_metadata.update(new_kernel1_data)

    # Now initial_strand_metadata has the new kernel data
    print(initial_strand_metadata)

    initial_strand = {
        'code': initial_strand_code,
        'metadata': initial_strand_metadata,
        'exons': exons_data  # Adding exons_data to initial_strand
    }

    dna_structure = {
        'Genomes': {
            'Chromosomes': {
                'Genes': {
                    'Nucleotide Sequences': {
                        'code': dna_structure_code,
                        'introns': {'mappings': rna_dna_mapper.mapping}  # Added introns here
                    }
                }
            }
        }
    }

    # Final JSON Data
    final_json_data = {
        'dna_structure': dna_structure,
        'initial_strand': initial_strand  # initial_strand now includes exons
    }

    # Add introns data
    introns_data = {'mappings': rna_dna_mapper.mapping}
    final_json_data['dna_structure']['Genomes']['Chromosomes']['Genes']['Nucleotide Sequences']['introns'] = introns_data

    # Convert the mappings to a single-line string
    mappings_str = json.dumps(rna_dna_mapper.mapping)
    mappings_str = mappings_str.replace(", ", ",")

    # Embed this one-liner into the DNA structure
    dna_structure['Genomes']['Chromosomes']['Genes']['Nucleotide Sequences']['introns'] = {'mappings': mappings_str}

    # Write most of the JSON data
    with open(output_path, 'w', encoding='utf-8') as json_file:
        # Serialize DNA structure and initial strand but exclude the 'introns' data for now
        json.dump({'dna_structure': dna_structure, 'initial_strand': initial_strand}, json_file, ensure_ascii=False, indent=4)
    
        # Close the JSON object
        json_file.write("\n}")  # Remove the extra line for 'introns'

    # Use FileProcessor to encode the final encoded_dna_data.json into chunks.json
    processor = FileProcessor(input_directory='outputs', output_directory='outputs')
    processor.compress_and_generate_base64_chunks('encoded_dna_data.json', output_file_name='chunks.json')

    # Read the contents of chunks.json as a string
    chunks_json_path = os.path.join(processor.output_directory, 'chunks.json')
    with open(chunks_json_path, 'r', encoding='utf-8') as chunks_file:
        chunks_data = chunks_file.read()

    # Create a dictionary for the initial_strand including the chunks field
    initial_strand_with_chunks = {
        'chunks': chunks_data,  # Include the chunks field here
        'code': initial_strand_code,
        'metadata': initial_strand_metadata,
        'exons': exons_data
    }

    # Serialize the initial_strand_with_chunks JSON structure
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump({'dna_structure': dna_structure, 'initial_strand': initial_strand_with_chunks}, json_file, ensure_ascii=False, indent=4)

    # Execute the companion script at the end
    subprocess.run(['python3', 'ai_dna_chunker.py'])
    subprocess.run(['python3', 'ai_dna_squashfs.py'])
    subprocess.run(['python3', 'ai_dna_chunksquash.py'])
    subprocess.run(['python3', 'ai_dna_os.py'])
    subprocess.run(['python3', 'ai_dna_os_fs.py'])

if __name__ == "__main__":
    main()
