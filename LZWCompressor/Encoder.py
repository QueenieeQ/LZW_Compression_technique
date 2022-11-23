from numba import jit



class Encoder:
    '''
    Data encoding with lossless compression algorithm (LZW)
    
    The class includes the following methods:
        __init__        - Object Initialization.
        init_trie       - Initializing the trie.
        trie_update     - Add item to trie.
        encode          - Encode data.

    *The dictionary is the trie.
    
    '''


    def __init__(self):

        # Initializing the trie
        self.init_trie()


    def init_trie(self):
        ''' Create and initializing the trie '''

        self.trie = {}       
        self.table_size = 0


    def trie_update(self, start_range, end_range):
        ''' Add a range of characters to the Trie '''

        if (start_range > end_range):
            print('invalid range !')

        else:      
            # Right border inclusive
            end_table = end_range - start_range + self.table_size + 1
            
            different = start_range - self.table_size

            for i in range(self.table_size, end_table):

                # Skip duplicate values
                if (chr(i + different) in self.trie):
                    continue

                else:
                    self.trie[chr(i + different)] = i
                    self.table_size += 1


    def encode(self, data, bits_number):
        ''' Given the number of bits, to encode the input data '''

        # Defining the maximum table size
        maximum_table_size = 2 ** int(bits_number)

        return _encode(data, self.trie, self.table_size, maximum_table_size)


@jit()
def _encode(data, trie, table_size, maximum_table_size):
    
    # List storing compressed data
    encoded_data = []
   
    prefix = ''

    for symbol in data:
        string = prefix + symbol
            
        if (string in trie):
            prefix = string

        else:
            encoded_data.append(trie[prefix])

            # Expand the table if the maximum table size is not exceeded
            if(len(trie) <= maximum_table_size - 1):
                trie[string] = table_size
                table_size += 1

            prefix = symbol
        
    # Add the last symbol of the input data
    if (prefix in trie):
        encoded_data.append(trie[prefix])

    return (encoded_data)
