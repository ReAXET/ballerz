"""Helper functions for decompressing zst files"""

import tempfile 
import tarfile
import os
import shutil
import zstandard as zstd

from pathlib import Path

import os
import zstandard as zstd




def decompress_zst_files(folder_path):
    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        raise ValueError("The provided path is not a directory.")

    # Get a list of files in the directory
    files = os.listdir(folder_path)

    # Iterate through the files
    for file in files:
        # Check if the file ends with '.zst'
        if file.endswith('.zst'):
            # Construct the full path to the zst file
            file_path = os.path.join(folder_path, file)
            # Construct the output file path
            output_file_path = os.path.splitext(file_path)[0]

            # Open the zst file for reading
            with open(file_path, 'rb') as compressed_file:
                # Create a Zstd decompressor
                decompressor = zstd.ZstdDecompressor()

                # Open the output file for writing
                with open(output_file_path, 'wb') as output_file:
                    # Decompress and write the data
                    decomp = decompressor.stream_reader(compressed_file)
                    for chunk in decomp:
                        output_file.write(chunk)

            print(f"Decompressed {file} to {output_file_path}")

# Example usage:
# decompress_zst_files('/path/to/your/folder')
