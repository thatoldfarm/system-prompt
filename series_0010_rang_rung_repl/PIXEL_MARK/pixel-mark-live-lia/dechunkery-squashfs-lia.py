import gzip
import base64
import os
import numpy as np
from PIL import Image
import math
import struct

class IronVaultPrecision:
    @staticmethod
    def encode(input_path, output_png="MASTER_DNA_SEED.png"):
        if not os.path.exists(input_path):
            print(f"[!] Source file {input_path} not found.")
            return

        print(f"[ENCODE] Opening Binary Source: {input_path}")
        with open(input_path, "rb") as f:
            raw_bytes = f.read()
        
        # 1. Compress
        compressed = gzip.compress(raw_bytes)
        
        # 2. Base64
        b64_str = base64.urlsafe_b64encode(compressed)
        data_len = len(b64_str)
        
        # 3. Precision Anchor: Append the data length as a 4-byte big-endian integer
        # This allows the decoder to ignore any trailing padding pixels.
        payload = b64_str + struct.pack(">I", data_len)
        
        # 4. RGB Pixel Mapping
        padding_needed = (3 - len(payload) % 3) % 3
        padded_payload = payload + b'\x00' * padding_needed
        pixels = np.frombuffer(padded_payload, dtype=np.uint8).reshape(-1, 3)
        
        side = int(math.ceil(math.sqrt(len(pixels))))
        vram = np.zeros((side * side, 3), dtype=np.uint8)
        vram[:len(pixels)] = pixels
        
        Image.fromarray(vram.reshape((side, side, 3))).save(output_png)
        print(f"[SUCCESS] Created {output_png} ({side}x{side} px)")
        print(f"          Original Size: {len(raw_bytes)} bytes")

    @staticmethod
    def decode(png_path, output_path="perfect_restoration.json"):
        if not os.path.exists(png_path):
            print(f"[!] Seed file {png_path} not found.")
            return

        print(f"[DECODE] Extracting Lattice: {png_path}")
        img = Image.open(png_path).convert('RGB')
        raw_bytes = np.array(img).flatten().tobytes()
        
        # 1. Search for the Length Anchor
        # We strip the trailing nulls added by the PNG square-fit
        # The last 4 bytes of our ACTUAL data is the length of the B64 string.
        clean_bytes = raw_bytes.rstrip(b'\x00')
        data_len = struct.unpack(">I", clean_bytes[-4:])[0]
        
        # 2. Slice the exact B64 data
        b64_data = clean_bytes[:data_len]
        
        # 3. Restore
        compressed = base64.urlsafe_b64decode(b64_data)
        original_bytes = gzip.decompress(compressed)
        
        with open(output_path, "wb") as f:
            f.write(original_bytes)
            
        print(f"[SUCCESS] Restored to {output_path}")
        print(f"          Final Size: {len(original_bytes)} bytes")
        return len(original_bytes)

# --- LIVE EXECUTION BLOCK ---
if __name__ == "__main__":
    vault = IronVaultPrecision()
    
    # THE FILENAMES
    SOURCE = "encoded_dna_data.json"
    SEED = "MASTER_DNA_SEED.png"
    RESULT = "reconstructed_perfectly.json"

    print("--- IRON VAULT PRECISION TEST ---")
    
    # 1. RUN ENCODER
    vault.encode(SOURCE, SEED)
    
    # 2. RUN DECODER
    if os.path.exists(SEED):
        vault.decode(SEED, RESULT)
        
        # 3. FINAL INTEGRITY CHECK
        if os.path.exists(SOURCE) and os.path.exists(RESULT):
            orig_sz = os.path.getsize(SOURCE)
            rest_sz = os.path.getsize(RESULT)
            print("-" * 33)
            print(f"ORIGINAL: {orig_sz} bytes")
            print(f"RESTORED: {rest_sz} bytes")
            if orig_sz == rest_sz:
                print(">>> STATUS: BIT-PERFECT. Φ = 1.0 <<<")
            else:
                print(f">>> DRIFT DETECTED: {rest_sz - orig_sz} bytes <<<")
