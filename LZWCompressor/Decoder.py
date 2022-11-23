from numba import jit



class Decoder:
    '''
    Data decoding with lossless compression algorithm (LZW)
    
    The class includes the following methods:
        __init__        - Object Initialization.
        init_trie       - Initializing the trie
        trie_update     - Add item to trie
        decode          - Decode data
        
    *The dictionary is the trie.
    
    '''


    def __init__(self):

        # Initializing the trie
        self.init_trie()


    def init_trie(self):
        ''' Create and initializing the trie '''

        self.trie = {}
        self.table_size = 0

        # Storing Trie values to avoid repetitions
        self.values = []


    def trie_update(self, start_range, end_range):
        ''' Add a range of characters to the Trie '''
      
        if (start_range > end_range):
            print('invalid range !')

        else:           
            # Right border inclusive
            end_table = end_range - start_range + self.table_size + 1
            
            different = start_range - self.table_size
            t = self.table_size

            for i in range(self.table_size, end_table):

                # Skip duplicate values
                if (chr(i + different) in self.values):
                    continue

                else:
                    self.trie[str(i)] = chr(i + different)
                    self.values.append(chr(i + different))
                    self.table_size += 1


    def decode(self, encoded_data, bits_number):
        ''' Decode the received data '''

        # Defining the maximum table size
        maximum_table_size = pow(2, int(bits_number))

        return _decode(encoded_data, self.trie, self.table_size, maximum_table_size)


@jit()
def _decode(encoded_data, trie, table_size, maximum_table_size):
    
    # List storing compressed data
    prefix = ''
    decoded_data = []

    for value in encoded_data:
        value = str(value)

        if not (value in trie):          
            trie[value] = prefix + prefix[0]

        decoded_data.append(trie[value])

        if len(prefix):
            if(len(trie) <= maximum_table_size - 1):
                trie[str(table_size)] = prefix + trie[value][0]
                table_size += 1
        prefix = trie[value]  

    decoded_data = ''.join(decoded_data)

    return decoded_data
