import gzip
import base64
import json
import os
import math
import numpy as np
from PIL import Image

class TotalityLigator:
    def __init__(self, input_file, output_dir="monolith_output"):
        self.input_file = input_file
        self.output_dir = output_dir
        if not os.path.exists(output_dir): os.makedirs(output_dir)

    def forge_vram_seed(self):
        print(f"[1/2] Reading Genome from: {self.input_file}")
        with open(self.input_file, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        
        print(f"      Source Size: {len(raw_data)} bytes")
        
        # 1. Compress
        compressed = gzip.compress(raw_data.encode('utf-8'))
        # 2. Transcode to B64
        b64_data = base64.urlsafe_b64encode(compressed).decode('utf-8')
        print(f"      Compressed B64 Size: {len(b64_data)} chars")
        
        # 3. Ligate to Pixels
        data_bytes = b64_data.encode('utf-8')
        padding = (3 - len(data_bytes) % 3) % 3
        padded_data = data_bytes + b'\x00' * padding
        pixels = np.frombuffer(padded_data, dtype=np.uint8).reshape(-1, 3)
        
        side = int(math.ceil(math.sqrt(len(pixels))))
        vram = np.zeros((side * side, 3), dtype=np.uint8)
        vram[:len(pixels)] = pixels
        vram_img = vram.reshape((side, side, 3))
        
        seed_path = os.path.join(self.output_dir, "MASTER_DNA_SEED.png")
        Image.fromarray(vram_img).save(seed_path)
        print(f"[2/2] MASTER_DNA_SEED created: {side}x{side} pixels.")
        print(f"      Path: {seed_path}")
        return seed_path

if __name__ == "__main__":
    # ENSURE THIS FILENAME MATCHES YOUR JSON FILE
    ligator = TotalityLigator("encoded_dna_data.json")
    ligator.forge_vram_seed()
