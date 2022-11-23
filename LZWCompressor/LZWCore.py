"""Reference.
Usage:
  LZWCore.py compress <FILE> [PATH] [-t]
  LZWCore.py decompress <FILE> [PATH] [-t]

Arguments:
  FILE        input file
  PATH        directory for saving converted file (optional)

Examples:
  LZWCore.py compress /temp/img.bmp /temp/compressed
  LZWCore.py decompress /temp/img.lzw /temp/decompressed

Options:
  -h, --help    Show reference.
  -t            Show lead time.

"""

from docopt import docopt

from numba import jit
import os.path
import struct
import time

import warnings
warnings.filterwarnings('ignore')

from Encoder import Encoder
from Decoder import Decoder



class LZWCore():
    ''' 
    Implementation of a universal lossless data compression 
    algorithm - LZW.

    The class includes the following main methods:
        compress        - Compress the file using the LZV algorithm.
        decompress      - Decompress the file using the LZV algorithm.
    '''
    
    def __init__(self):
        ''' 
        Init Encoder and Decoder.
        Adding selected ranges to encoder and decoder dictionaries.
        
        '''

        # Encoder init
        self.encoder = Encoder()
        self.reset_encoder()

        # Decoder init
        self.decoder = Decoder()
        self.reset_decoder()


    def reset_encoder(self) -> None:
        ''' Adding selected ranges to encoder dictionaries. '''

        self.encoder.init_trie()

        # ASCII punctuation and symbols
        self.encoder.trie_update(32, 47)
        self.encoder.trie_update(58, 64)
        self.encoder.trie_update(91, 96)
        self.encoder.trie_update(123, 126)

        # ASCII digits
        self.encoder.trie_update(48, 57)

        # Latin alphabet
        self.encoder.trie_update(65, 90)
        self.encoder.trie_update(97, 122)


    def reset_decoder(self) -> None:
        ''' Adding selected ranges to decoder dictionaries. '''

        self.decoder.init_trie()

        # ASCII punctuation and symbols
        self.decoder.trie_update(32, 47)
        self.decoder.trie_update(58, 64)
        self.decoder.trie_update(91, 96)
        self.decoder.trie_update(123, 126)

        # ASCII digits
        self.decoder.trie_update(48, 57)

        # Latin alphabet
        self.decoder.trie_update(65, 90)
        self.decoder.trie_update(97, 122)


    # -------------------------- COMPRESS --------------------------- #
    def read_file_binary(self, path: str) -> str:
        ''' Open a file in binary mode and read the whole file. '''

        with open(path, 'rb') as file:
            file_content = str(file.read())
        file_content = file_content[2:-1] # remove b''

        return file_content


    def save_compress_file(self, 
                           encoded_data: list, 
                           output_path: str, 
                           path: str) -> None:
        ''' 
        Using an external "_save_compress_file" function to save a 
        compressed file with a ".lzw" extension.
        
        '''

        _save_compress_file(encoded_data, output_path, path)


    def compress(self, 
                 path: str, 
                 output_path: str, 
                 time_flag: bool = False) -> None:
        '''  Compress the file using the LZV algorithm. '''

        lead_time = time.time()

        file_content = self.read_file_binary(path)
        encoded_data = self.encoder.encode(file_content, 32)       
        self.save_compress_file(encoded_data, output_path, path)

        lead_time = time.time() - lead_time
        if time_flag:
            print('Compress - Lead time:', str(lead_time) + 's.')


    # ------------------------- DECOMPRESS -------------------------- #
    def read_compress_file(self, path: str) -> list:
        ''' 
        Using an external "_read_compress_file" function 
        to read a ".lzw" file .
        
        '''

        compressed_data = _read_compress_file(path)
        return compressed_data


    def save_decompress_file(self, 
                             decompressed_data: str, 
                             path: str, 
                             output_path: str) -> None:
        ''' Save the decompressed file to "output_path" directory. '''
           
        # Processing '\' and '/' paths.
        file_name = path.split('\\')[-1]
        file_name = file_name.split('/')[-1].replace('.lzw', '')

        with open(output_path + file_name, 'wb') as file:
            file.write(decompressed_data)


    def decompress(self, 
                   path: str, 
                   output_path: str,
                   time_flag: bool = False) -> None:
        ''' Decompress the file using the LZV algorithm. '''

        lead_time = time.time()

        compressed_data = self.read_compress_file(path)

        decompressed_data = self.decoder.decode(compressed_data, 32)
        decompressed_data = "b'" + decompressed_data + "'"
        decompressed_data = eval(decompressed_data)

        self.save_decompress_file(decompressed_data, path, output_path)

        lead_time = time.time() - lead_time
        if time_flag:
            print('Decompress - Lead time:', str(lead_time) + 's.')


@jit()
def _save_compress_file(encoded_data: list, 
                        output_path: str, 
                        path: str) -> None:
    ''' Save a compressed file with a ".lzw" extension.  '''

    # Processing '\' and '/' paths.
    file_name = path.split('\\')[-1]
    file_name = file_name.split('/')[-1] + '.lzw'

  
    # numba doesn't support WITH statement!!!
    file = open(output_path + file_name, 'wb')

    for data in encoded_data:
        file.write(struct.pack('>I', int(data)))  
    file.close()
    


@jit()
def _read_compress_file(path: str) -> list:
    ''' Read a ".lzw" file. '''

    compressed_data = []

    # numba doesn't support WITH statement!!!
    file = open(path, 'rb')

    while True:
        rec = file.read(4)
        if len(rec) != 4:
            break
        (data, ) = struct.unpack('>I', rec)
        compressed_data.append(data)
    file.close()

    return compressed_data


def main():
    # DocOpt
    arguments = docopt(__doc__)

    # Validation
    if arguments['compress']:
        mode = 'c'
    else:
        mode = 'd'

    file = arguments['<FILE>']
    if not(os.path.isfile(file)):
        print('File is not found!')
        return

    if mode == 'd':
        if (file.split('.')[-1] != 'lzw'):
            print('Need .lzw file!')
            return

    output = arguments['PATH']
    if (output == None) or (os.path.isfile(output)) or (not(os.path.exists(output))):
        # By default, save the file next to the executable.
        output = '.\\'

    time_flag = arguments['-t']

    # Process
    core = LZWCore()

    if mode == 'c':
        try:
            core.compress(file, output, time_flag)
        except:
            print('Compress Error!')
    else:
        try:
            core.decompress(file, output, time_flag)
        except:
            print('Decompress Error!')
    


if __name__ == '__main__':
    main()




