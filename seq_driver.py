import pdb
import csv
import tables as tb

import argparse

import sequences

def seq_driver_incr(max_initial,length,verbose=False):
    """
    Calculate a dictionary of many Fibonacci-like sequences.  Each entry
    in the dictionary uses a different number of previous numbers to formulate
    the sum for the next entry.  The number of previous numbers is the list from
    2 to `max_initial`.

    input:
    ------
    max_initial : (integer) indicates the number of entries to sum for the 
                  next entry in the largest case
    length : (integer) the number of entries to include in the sequence
    verbose : (bool) whether or not to print extra output [optional]

    output:
    -------
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """

    return seq_driver_generic(list(range(2,max_initial+1)), length, verbose)

    
def seq_driver_generic(initial_list, length, verbose=False):
    """
    Calculate a dictionary of many Fibonacci-like sequences.  Each entry
    in the dictionary uses a different number of previous numbers to formulate
    the sum for the next entry.  The number of previous numbers is indicated
    in the `initial_list`.

    input:
    ------
    initial_list : (integer) indicates the list of different values to use as
                   the number of entries to sum for the next entry in each case
    length : (integer) the number of entries to include in the sequence
    verbose : (bool) whether or not to print extra output [optional]

    output:
    -------
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """
    
    seq_dict = {}
    for init in initial_list:
        seq_dict[(init,length)] = sequences.calc_sequence(init,length,verbose)

    return seq_dict

def seq_dict_str(seq_dict):
    """
    Generate a string version of a sequence dictionary in the format:
    key : sequence
    where key is the tuple that defines the sequence and sequence is the list of integers.

    inputs:
    -------
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers

    outputs:
    --------
    seq_string : (string) formatted as above
    """
    
    return "\n".join(["{0} : {1}".format(key,val) for key,val in seq_dict.items()])

def write_seq_dict_txt(filename, seq_dict):
    """
    Print a sequence dictionary to standard out in the format:
    key : sequence
    where key is the tuple that defines the sequence and sequence is the list of integers.

    inputs:
    -------
    filename : (string) the name of the file to write
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    
    """

    with open(filename, 'w') as file:
        file.write(seq_dict_str(seq_dict))

    
def write_seq_dict_csv(filename, seq_dict):
    """
    Write a sequence dictionary to a CSV formatted file with heading.
    The headings are 'initial' and 'length' followed by a list of values `S<n>` where
    `<n>` ranges from 0 to the length of the sequence-1.
    The heading is autocomputed from the length of the sequences in the dictionary.

    inputs:
    -------
    filename : (string) the name of the file to write
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """

    seq_length = len(list(seq_dict.values())[0])
    seq_headings = ['initial','length'] + ["S" + str(idx) for idx in range(seq_length)]
    
    with open(filename, "w") as csvfile:
        seq_writer = csv.writer(csvfile,delimiter=',')
        seq_writer.writerow(seq_headings)
        for key,val in seq_dict.items():
            seq_writer.writerow(list(key)+val)
    

seq_group_name = 'sequences'
    
def get_existing_seqs(h5file):
    """
    Get a list of the sequnces that are already stored in the file.

    inputs:
    -------
    h5file : a file handle for an open HDF5 file

    outputs:
    --------
    seq_list : set(tuple(init,length)) set of existing sequences defined by their 
               initial number and length
    """
    
    seq_list = set()
    for seq in h5file.walk_nodes('/' + seq_group_name,'Array'):
        seq_list.add((seq.attrs.init,seq.attrs.length))

    return seq_list

def write_seq_dict_hdf5(filename, seq_dict):
    """
    Write a sequence dictionary to an HDF5 formatted file.
    
    A new group will be 

    inputs:
    -------
    filename : (string) the name of the file to write
    seq_dict : dict{(initial,length) : list(integer)} dictionary of all the 
               resulting sequences of integers
    """

    f = tb.open_file(filename, 'a')

    try:
        seq_node = f.get_node('/' + seq_group_name)
        seq_list = get_existing_seqs(f)
        seq_idx = len(seq_list)
    except tb.NoSuchNodeError:
        f.create_group('/', seq_group_name, "My Sequences")
        seq_list = set()
        seq_idx = 0

    for key,val in seq_dict.items():
        if key not in seq_list:
            seq_name = "seq"+str(seq_idx)
            seq_array = f.create_array('/' + seq_group_name,seq_name,val)
            seq_array.attrs.init = key[0]
            seq_array.attrs.length = key[1]
            seq_idx += 1

    f.close()
                                   
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--max_number", type=int, default=2, required=False,
                        help="Determines the range of initial numbers are used/necessary to compute the sequence.")

    parser.add_argument("-l", "--length", type=int, default=10, required=False,
                        help="Determines how many terms in the sequence to calculate and print.")

    parser.add_argument("-f", "--filename", type=str, default="sequences.txt", required=False,
                        help="Filename to store sequences in CSV version.")

    parser.add_argument("-F", "--format", type=str, default="txt", required=False, choices=['txt','csv','hdf'],
                        help="Choose the file format.")
    
    parser.add_argument("-v", "--verbose", action='store_true', required=False,
                        help="Print extra information to the screen during calculation.")

    args = parser.parse_args()

    seq_dict = seq_driver_incr(args.max_number, args.length, args.verbose)

    if args.verbose:
        print(seq_dict_str(seq_dict))

    if args.format == 'csv':
        write_seq_dict_csv(args.filename,seq_dict)
    elif args.format == 'txt':
        write_seq_dict_txt(args.filename,seq_dict)
    elif args.format == 'hdf':
        write_seq_dict_hdf5(args.filename,seq_dict)
        

        
