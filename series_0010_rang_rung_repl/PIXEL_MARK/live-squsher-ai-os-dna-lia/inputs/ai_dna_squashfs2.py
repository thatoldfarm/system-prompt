import subprocess
import os

def create_squashfs(input_directory, output_file):
    try:
        # Run the mksquashfs command to create a SquashFS file system
        subprocess.run(["mksquashfs", input_directory, output_file], check=True)
        print(f"SquashFS file system created: {output_file}")
    except subprocess.CalledProcessError:
        print("An error occurred while creating the SquashFS file system.")

if __name__ == "__main__":
    # Define the input directory and the output SquashFS file
    input_directory = "outputs"
    output_file = "outputs2.squashfs"

    # Check if the mksquashfs command is available
    try:
        subprocess.run(["mksquashfs", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("mksquashfs is not installed. Please install it and try again.")
        exit(1)
    except FileNotFoundError:
        print("mksquashfs is not installed. Please install it and try again.")
        exit(1)

    # Create the SquashFS file system
    create_squashfs(input_directory, output_file)
