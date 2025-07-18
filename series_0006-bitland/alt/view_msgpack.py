import msgpack
import json

def view_msgpack(msgpack_file):
    with open(msgpack_file, 'rb') as f:
        data = msgpack.load(f)
    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    msgpack_file = 'LIA_MASTER_BOOTSTRAP_v15_Omniversal_Nexus_Prime_Genesis.msgpack'
    view_msgpack(msgpack_file)
