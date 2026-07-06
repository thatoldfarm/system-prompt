import gzip
import base64
import os
import numpy as np
from PIL import Image
import math
import struct
import json
import hashlib
import sys

class IronVaultUltimate:
    def __init__(self):
        self.prefix = "MASTER_DNA_SEED_"
        self.output_ext = ".png"

    def _calculate_checksum(self, data):
        """Generates a SHA-256 hash of the data for integrity verification."""
        return hashlib.sha256(data).hexdigest()

    def encode_batch(self, input_dir="pixelate", output_dir="pixelated"):
        """Converts files in input_dir into data-embedded PNGs in output_dir."""
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
            print(f"[*] Created '{input_dir}/' folder. Place files there and run again.")
            return

        os.makedirs(output_dir, exist_ok=True)
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

        if not files:
            print(f"[!] No files found in '{input_dir}' to encode. Skipping.")
            return

        print(f"\n--- PHASE 1: ENCODING (Source: {input_dir}) ---")

        for filename in files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{self.prefix}{filename}{self.output_ext}")

            print(f"[+] Encoding: {filename}")

            with open(input_path, "rb") as f:
                raw_data = f.read()

            checksum = self._calculate_checksum(raw_data)
            metadata = {
                "filename": filename,
                "checksum": checksum,
                "size": len(raw_data)
            }
            metadata_json = json.dumps(metadata).encode('utf-8')
            compressed_data = gzip.compress(raw_data)

            # Package structure: [Header Len] + [Header] + [Data]
            header_len_bin = struct.pack(">I", len(metadata_json))
            payload = header_len_bin + metadata_json + compressed_data

            b64_str = base64.urlsafe_b64encode(payload)
            # Precision Anchor at the very end
            final_data = b64_str + struct.pack(">I", len(b64_str))

            padding = (3 - len(final_data) % 3) % 3
            padded_data = final_data + b'\x00' * padding
            pixels = np.frombuffer(padded_data, dtype=np.uint8).reshape(-1, 3)

            side = int(math.ceil(math.sqrt(len(pixels))))
            vram = np.zeros((side * side, 3), dtype=np.uint8)
            vram[:len(pixels)] = pixels

            Image.fromarray(vram.reshape((side, side, 3))).save(output_path)
            print(f"    Success: Created {os.path.basename(output_path)}")

    def decode_batch(self, input_dir="pixelated", output_dir="pixelated_done"):
        """Converts PNGs in input_dir back into original files in output_dir."""
        if not os.path.exists(input_dir):
            print(f"[!] Input directory '{input_dir}' not found. Skipping.")
            return

        os.makedirs(output_dir, exist_ok=True)
        files = [f for f in os.listdir(input_dir) if f.endswith(self.output_ext) and f.startswith(self.prefix)]

        if not files:
            print(f"[!] No valid IronVault PNGs found in '{input_dir}'. Skipping.")
            return

        print(f"\n--- PHASE 2: DECODING (Source: {input_dir}) ---")

        for png_file in files:
            img_path = os.path.join(input_dir, png_file)
            print(f"[+] Analyzing: {png_file}")

            try:
                img = Image.open(img_path).convert('RGB')
                raw_bytes = np.array(img).flatten().tobytes()

# We search backwards to find the exact length anchor.
                # Since the anchor is struct.pack(">I", len(b64_str)),
                # the value of the anchor must match its index in the raw_bytes array.
                total_b64_len = 0
                for i in range(len(raw_bytes) - 4, -1, -1):
                    length = struct.unpack(">I", raw_bytes[i:i+4])[0]
                    if length == i:
                        total_b64_len = length
                        clean_bytes = raw_bytes[:i+4]
                        break

                if total_b64_len == 0:
                    raise ValueError("Could not find valid Precision Anchor")

                b64_payload = clean_bytes[:total_b64_len]
                binary_blob = base64.urlsafe_b64decode(b64_payload)

                header_len = struct.unpack(">I", binary_blob[:4])[0]
                metadata_json = binary_blob[4:4+header_len]
                metadata = json.loads(metadata_json.decode('utf-8'))

                compressed_data = binary_blob[4+header_len:]
                restored_data = gzip.decompress(compressed_data)

                new_checksum = self._calculate_checksum(restored_data)
                status = "BIT-PERFECT VERIFIED" if new_checksum == metadata['checksum'] else "!!! DATA CORRUPTED !!!"

                output_path = os.path.join(output_dir, os.path.basename(metadata['filename']))
                with open(output_path, "wb") as f:
                    f.write(restored_data)

                print(f"    Restored: {metadata['filename']} | {status}")

            except Exception as e:
                print(f"    [!] FAILED to process {png_file}: {e}")

# --- AUTO-SENSING COMMAND CENTER ---
if __name__ == "__main__":
    vault = IronVaultUltimate()

    print("==============================")
    print("    IRON VAULT ULTIMATE v3    ")
    print("==============================")

    # Logic for automatic execution
    if len(sys.argv) > 1:
        # User provided a flag
        cmd = sys.argv[1].lower()
        if cmd in ['e', 'encode']:
            vault.encode_batch("pixelate", "pixelated")
        elif cmd in ['d', 'decode']:
            vault.decode_batch("pixelated", "pixelated_done")
        else:
            print(f"Unknown flag '{cmd}'. Use 'encode' or 'decode'.")
    else:
        # NO FLAG PROVIDED: Do both automatically
        print("[*] No flags provided. Running FULL VAULT CYCLE (Encode + Decode)...")
        vault.encode_batch("pixelate", "pixelated")
        vault.decode_batch("pixelated", "pixelated_done")
        print("\n--- ALL TASKS COMPLETE ---")
