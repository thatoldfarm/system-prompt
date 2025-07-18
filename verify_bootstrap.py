import json
import os

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def verify_bootstrap(master_file):
    master_data = load_json_file(master_file)
    for key, value in master_data.items():
        if isinstance(value, dict) and '$ref' in value:
            ref_file = os.path.join(os.path.dirname(master_file), value['$ref'])
            if os.path.exists(ref_file):
                print(f"Found referenced file: {ref_file}")
                verify_bootstrap(ref_file)
            else:
                print(f"Error: Referenced file not found: {ref_file}")
                return False
    return True

if __name__ == '__main__':
    master_file = 'series_0006-bitland/LIA_MASTER_BOOTSTRAP_v16_Bitland_Genesis.json'
    if verify_bootstrap(master_file):
        print("Bootstrap verification successful!")
    else:
        print("Bootstrap verification failed.")
