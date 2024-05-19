"""Functions that help with zstandard compression and decompression."""
import os
import zstandard as zstd

def compress_file(input_file, output_file):
    """Compresses a file using zstandard."""
    with open(input_file, 'rb') as input_f:
        input_data = input_f.read()
    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(input_data)
    with open(output_file, 'wb') as output_f:
        output_f.write(compressed_data)


def decompress_ztsd_files(directory):
    """Decompresses all .zst files in a directory.
    

    Args:
        directory (str): The directory containing the .zst files to decompress.
    
    Example: 
        directory_path = 'path/to/directory'
        decompress_ztsd_files(directory_path)
    """
    for file in os.listdir(directory):
        if file.endswith('.zst'):
            file_path = os.path.join(directory, file)
            output_file = file_path[:-4] or os.path.join(directory, file.split('.')[0])

            # Open input file .zst and read data
            with open(file_path, 'rb') as compressed_f:
                # Create decompressor object
                decompressor_dctx = zstd.ZstdDecompressor()
                
                # Open output file and write decompressed data
                with open(output_file, 'wb') as output_f:
                    decompressor_dctx.copy_stream(compressed_f, output_f)

            # Remove compressed file
            os.remove(file_path)


