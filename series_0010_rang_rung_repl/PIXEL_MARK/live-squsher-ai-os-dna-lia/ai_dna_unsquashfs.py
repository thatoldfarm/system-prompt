import subprocess
import os
import shutil

def decompress_squashfs(input_file='outputs.squashfs', output_directory='unsquash'):
    # Remove the output directory if it exists
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    # Run the unsquashfs command to decompress the SquashFS file
    command = ['unsquashfs', '-d', output_directory, input_file]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully decompressed {input_file} to {output_directory}")
    except subprocess.CalledProcessError:
        print(f"Failed to decompress {input_file}")

if __name__ == '__main__':
    decompress_squashfs()
