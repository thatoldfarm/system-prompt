from bson import BSON
import json

def view_bson(bson_file):
    with open(bson_file, 'rb') as f:
        data = BSON(f.read()).decode()
    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    bson_file = 'LIA_MASTER_BOOTSTRAP_v15_Omniversal_Nexus_Prime_Genesis.bson'
    view_bson(bson_file)
