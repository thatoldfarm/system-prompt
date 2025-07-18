import json
import msgpack
from bson import BSON
import os

def convert_bootstrap(json_file, output_dir):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Convert to MessagePack
    msgpack_file = os.path.join(output_dir, os.path.basename(json_file).replace('.json', '.msgpack'))
    with open(msgpack_file, 'wb') as f:
        msgpack.dump(data, f)

    # Convert to BSON
    bson_file = os.path.join(output_dir, os.path.basename(json_file).replace('.json', '.bson'))
    with open(bson_file, 'wb') as f:
        f.write(BSON.encode(data))

if __name__ == '__main__':
    json_file = 'series_0005-machina-urbs/002_ridgeline/LIA_MASTER_BOOTSTRAP_v15_Omniversal_Nexus_Prime_Genesis.json'
    output_dir = 'series_0006-bitland/alt'
    convert_bootstrap(json_file, output_dir)
