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

def print_seq_dict(seq_dict):

    print("\n".join(["{0} : {1}".format(key,val) for key,val in seq_dict.items()]))


if __name__ == "__main__":

    pass
